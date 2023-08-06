from datetime import datetime
import re
import flatdict
import wikitextparser
from wikitextparser import WikiText


class WikiTextMapper:
    def __init__(self):
        pass

    def __remove_ref_tags(self, text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<ref.*?ref>')
        return re.sub(clean, '', text)

    def extract_all_revisions_links(self, json_file):
        """ Extract of revisions links

        Args:
            json_file:

        Returns:

        """
        dic = {"page_name": json_file['title'].split(":")[-1], "revision": {}}
        for i in json_file['revision']:
            date_time_str = i['timestamp']
            date_time_obj = datetime.strptime(date_time_str,
                                              '%Y-%m-%dT%H:%M:%S.%f%z')
            if ('text' not in i) or '_VALUE' not in i['text']:
                dic["revision"][date_time_str] = []
                continue
            destination_pages = self.extract_links(i['text']['_VALUE'])
            dic["revision"][date_time_str] = destination_pages
        return dic

    def extract_links(self, wikitext: str) -> list:
        """ Extract all links in wikipedia source
        Args:
            wikitext: page wiki source
        Returns:
            List of target links
        """
        links = re.findall('\[\[([^\]\]]*)\]\]', wikitext)
        destination_pages = []
        for link in links:
            if ":" in link:
                continue
            else:
                if "|" in link:
                    destination_pages.append(link.split("|")[1])
                else:
                    destination_pages.append(link)
        return destination_pages

    def extract_infobox_properties(self, wikitext: str) -> dict:
        """Extract properties from source of a wikipedia page
        Args:
            wikitext: A source code of a page in wikipedia

        Returns:
            Flat dictionary which contains infobox properties
        """
        parsed_wikitext = WikiText(self.__remove_ref_tags(wikitext))
        dic = {}
        for template in parsed_wikitext.templates:
            if "Infobox" in template.name:
                print(template.name)
                # for arg in template.arguments:
                #     dic[arg.name.strip()] = WikiText(arg.value).plain_text().strip()
                dic = self.template_properties(template)
                break
        d = flatdict.FlatDict(dic, delimiter='.')
        return dict(d)

    def template_properties(self, template: wikitextparser.Template) -> dict:
        """ Extract properties of wikipedia template
        Args:
            template: wikipedia template
        Returns:
            Flat dictionary which contains properties of the template
        """
        dic = {}
        for arg in template.arguments:
            if len(arg.templates) == 0 and len(arg.wikilinks) == 0:
                dic[arg.name.strip()] = arg.value.strip()
            elif len(arg.templates) == 0 and len(arg.wikilinks) != 0:
                continue
            elif len(arg.templates) > 0:
                c = 1
                for temp in arg.templates:
                    if temp.nesting_level == template.nesting_level + 1:
                        if f"{arg.name.strip()}.{temp.name}" in dic:
                            property_key = f"{arg.name.strip()}.{temp.name}{c}"
                            c += 1
                        else:
                            property_key = f"{arg.name.strip()}.{temp.name}"
                        dic[property_key] = self.template_properties(temp)
            else:
                print("Not defined")
        return dic

    def extract_infobox_links(self, wikitext: str) -> dict:
        """Extract links of a page's infobox
        Args:
            wikitext: A source code of a page in wikipedia

        Returns:
            Flat dictionary which contains infobox links
        """
        parsed_wikitext = WikiText(self.__remove_ref_tags(wikitext))
        dic = {}
        for template in parsed_wikitext.templates:
            if "Infobox" in template.name:
                print(template.name)
                dic = self.template_links(template)
                break
        d = flatdict.FlatDict(dic, delimiter='.')
        return dict(d)

    def template_links(self, template: wikitextparser.Template) -> dict:
        """ Extract links of wikipedia template
        Args:
            template: wikipedia template
        Returns:
            Flat dictionary which contains links of the template
        """
        dic = {}
        for arg in template.arguments:
            if len(arg.templates) == 0 and len(arg.wikilinks) != 0:
                dic[arg.name.strip()] = [link.target for link in
                                         WikiText(arg.value.strip()).wikilinks]
            elif len(arg.wikilinks) == 0:
                continue
            elif len(arg.templates) > 0:
                c = 1
                for temp in arg.templates:
                    if temp.nesting_level == template.nesting_level + 1:
                        if f"{arg.name.strip()}.{temp.name}" in dic:
                            property_key = f"{arg.name.strip()}.{temp.name}{c}"
                            c += 1
                        else:
                            property_key = f"{arg.name.strip()}.{temp.name}"
                        dic[property_key] = self.template_links(temp)
            else:
                print("Not defined")
        return dic

    def extract_plaintext(self, wikitext: str) -> str:
        pass
