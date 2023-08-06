# mkdocs-asciinema

A Mkdocs Plugin for asciinema player.

## Setup

Install the plugin using pip:

`pip install mkdocs-asciinema`

Activate the plugin in `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/asciinema-player.css

extra_javascript:
  - javascripts/asciinema-player.min.js

plugins:
  - search
  - mkdocs-asciinema
```

## Usage

```markdown
![asciicast](/images/asciinema/tmpzuu_levn-ascii.cast)
```
