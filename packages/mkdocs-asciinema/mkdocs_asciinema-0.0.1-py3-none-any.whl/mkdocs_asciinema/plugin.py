from mkdocs.plugins import BasePlugin

from bs4 import BeautifulSoup


class MkdocsAsciinemaPlugin(BasePlugin):

    def on_post_page(self, output_content, config, page, **kwargs):
        if 'alt="asciicast"' not in output_content:
            return output_content
        soup = BeautifulSoup(output_content, 'html.parser')
        asciicast_elements = soup.findAll("img", {"alt": "asciicast"})
        asciicasts = []
        for idx, element in enumerate(asciicast_elements):
            asciicast_id = f'asciicast-{idx}'
            asciicast_src = element.attrs['src']
            div_tag = soup.new_tag("div", id=asciicast_id)
            element.replace_with(div_tag)
            asciicasts.append(
                f'AsciinemaPlayer.create("{asciicast_src}", document.getElementById("{asciicast_id}"), {{ "fit": "width" }});')
        asciicast_script = soup.new_tag("script")
        asciicast_script.append("\n".join(asciicasts))
        soup.body.append(asciicast_script)
        return str(soup)
