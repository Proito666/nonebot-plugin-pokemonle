from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from nonebot_plugin_htmlrender import html_to_pic

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "resources/templates"),
    autoescape=True,
    enable_async=True
)
width=400
height=300

async def render_result(ans) -> bytes:
    template = env.get_template("guess.html")
    html = await template.render_async(ans)
    return await html_to_pic(html, viewport={"width": width, "height": height})
