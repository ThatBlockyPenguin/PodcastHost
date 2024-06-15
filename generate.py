from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import os
from typing import Any, Callable, TypeVar
from podgen import Podcast, Person, Episode, Media
import urllib.parse
import strictyaml as yaml
from shutil import copy

config_file = "config.yaml"
config_schema = yaml.Map({
    "files_data": yaml.Map({
        "episodes_folder": yaml.Str(),
        "info_file_name": yaml.Str()
    }),
    "podcast_data": yaml.Map({
        "title": yaml.Str(),
        "description": yaml.Str(),
        "author": yaml.Map({
            "name": yaml.Str(),
            "email": yaml.Email()
        }),
        "language": yaml.Str(),
        "webpage": yaml.Url(),
        "logo_url": yaml.Url()
    })
})
episode_info_schema = yaml.Map({
    "title": yaml.Str(),
    "date": yaml.Map({
        "day": yaml.Int(),
        "month": yaml.Int(),
        "year": yaml.Int()
    }),
    "credits": yaml.UniqueSeq(yaml.Str()),
    "description": yaml.Str(),
    "audio_file": yaml.Str()
})


@dataclass
class ConfigInfo:
    name: str
    data: yaml.YAML


with open(config_file, 'r') as file:
    try:
        config = yaml.load(file.read(), config_schema, config_file)
    except yaml.YAMLValidationError as e:
        print(e)
        quit(-2)


T = TypeVar('T')


def conf(key: str, *, cast: Callable[[Any], T] = str, config=ConfigInfo(config_file, config)) -> T:
    value = config.data

    for subkey in key.split("."):
        if not subkey in value:
            print(f'Config value "{subkey}" not found in {config.name}! Please create it.')
            quit(-1)
        value = value[subkey]

    return cast(value.value)


episodes_dir = os.path.join("./", conf("files_data.episodes_folder"))
about_path = conf("files_data.info_file_name")
podcast_title = conf("podcast_data.title")
podcast_desc = conf("podcast_data.description")
podcast_author_name = conf("podcast_data.author.name")
podcast_author_email = conf("podcast_data.author.email")
podcast_language = conf("podcast_data.language")
podcast_webpage = conf("podcast_data.webpage")
podcast_logo_url = conf("podcast_data.logo_url")


if not podcast_webpage.endswith("/"):
    podcast_webpage += "/"

episodes = [
    os.path.join(episodes_dir, episode)
    for episode
    in os.listdir(episodes_dir)
]

p = Podcast(
    name=podcast_title,
    description=podcast_desc,
    website=podcast_webpage,
    explicit=False,
    image=podcast_logo_url,
    language=podcast_language,
    authors=[Person(podcast_author_name, podcast_author_email)],
    feed_url=urllib.parse.urljoin(podcast_webpage, "rss.xml"),
    generator=None
)

for episode_path in episodes:
    with open(os.path.join(episode_path, about_path), "r") as info_file:
        info_file_name = os.path.normpath(info_file.name)

        try:
            episode_info = yaml.load(info_file.read(), episode_info_schema, info_file_name)
        except yaml.YAMLValidationError as e:
            print(e)
            quit(-2)

    info_config_meta = ConfigInfo(info_file_name, episode_info)
    episode_audio_path = os.path.join(
        episode_path,
        conf("audio_file", config=info_config_meta)
    )

    url = urllib.parse.urljoin(
        urllib.parse.urljoin(podcast_webpage, episodes_dir) + "/",
        "/".join([
            urllib.parse.quote(seg.replace("\\", "/"))
            for seg
            in os.path.relpath(episode_audio_path, episodes_dir).split("/")
        ])
    )

    episode_media = Media(
        url=url,
        size=os.path.getsize(episode_audio_path)
    )

    episode_media.populate_duration_from(episode_audio_path)

    title = conf("title", config=info_config_meta)
    date = datetime(
        day=conf("date.day", cast=int, config=info_config_meta),
        month=conf("date.month", cast=int, config=info_config_meta),
        year=conf("date.year", cast=int, config=info_config_meta),
        tzinfo=timezone(timedelta())
    )

    p.add_episode(
        Episode(
            title=title,
            summary=f"{title}, {date.strftime("%d/%m/%Y")}",
            long_summary=conf("description", config=info_config_meta),
            media=episode_media,
            publication_date=date
        )
    )

p.rss_file("rss.xml")
