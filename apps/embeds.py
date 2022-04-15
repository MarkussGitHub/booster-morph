import discord

#modified discord.Embed object
class Embed:
    def __init__(self):
        self = discord.Embed(
            name="Morph BOT",
            icon_url="https://i.imgur.com/tVGDT8m.png"
        )


    def warning(self, **kwargs) -> discord.Embed:
        self.color = 0xfae84a
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.fields = []
        self.footer = None
        self.image = None
        self.thumbnail = None

        return self

    def error(self, **kwargs) -> discord.Embed:
        self.color = 0xff0000
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.fields = []
        self.footer = None
        self.image = None
        self.thumbnail = None

        return self

    def info(self, **kwargs) -> discord.Embed:
        self.color = 0x00bfff
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.fields = []
        self.footer = None
        self.image = None
        self.thumbnail = None

        return self

    def add_field(self, name, value, inline=True) -> discord.Embed:
        """Adds a field to the embed object."""

        field = {
            "inline": inline,
            "name": name,
            "value": value,
        }

        try:
            self.fields.append(field)
        except AttributeError:
            self.fields = [field]

        return self

    def set_footer(self, text, icon_url=None) -> discord.Embed:
        """Sets the footer for the embed content."""

        self.footer = {
            "text": text,
            "icon_url": icon_url
        }

        return self

    def to_dict(self) -> dict:
        """Converts this embed object into a dict."""

        result = {
            "color": self.color,
            "title": self.title,
            "description": self.description,
            "fields": getattr(self, "fields", None),
            "footer": getattr(self, "footer", None),
            "image": getattr(self, "image", None),
            "thumbnail": getattr(self, "thumbnail", None),
        }

        return result

    def set_image(self, *, url):
        """Sets the image for the embed content."""

        self.image = {
            'url': str(url)
        }

        return self

    def set_thumbnail(self, *, url):
        """Sets the thumbnail for the embed content."""

        self.thumbnail = {
            'url': str(url)
        }

        return self