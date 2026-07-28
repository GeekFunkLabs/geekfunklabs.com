import os
import xml.etree.ElementTree as ET

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geekfunklabs.settings')
django.setup()

from blog.models import BlogPost, Tag
from markdownify import markdownify as md

FILE = "gfl_export.xml"
WP_NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

tree = ET.parse(FILE)
root = tree.getroot()
channel = root.find("channel")

for item in channel.findall("item"):
    if item.findtext("wp:post_type", namespaces=WP_NS) != "post":
        continue

    title = item.findtext("title")
    slug = item.findtext("wp:post_name", namespaces=WP_NS)
    
    published = True if item.findtext("wp:status", namespaces=WP_NS) == "publish" else False
    created = item.findtext("wp:post_date", namespaces=WP_NS)
    updated = item.findtext("wp:post_modified", namespaces=WP_NS)

    body_md = md(item.findtext("content:encoded", namespaces=WP_NS))

    tags = {}
    for tag in item.findall("category"):
        tags[tag.get("nicename")] = tag.text

    comments = []
    for comment in item.findall("wp:comment", namespaces=WP_NS):
        comments.append(dict(
            author=comment.findtext("wp:comment_author", namespaces=WP_NS),
            email=comment.findtext("wp:comment_author_email", namespaces=WP_NS),
            date=comment.findtext("wp:comment_date", namespaces=WP_NS),
            comment=comment.findtext("wp:comment_content", namespaces=WP_NS),
        ))

    """
    print("-------------------\n")
    print(f"{title} [{slug}] [published: {published}]")
    print(f"created: {created}, updated: {updated}")
    if tags:
        print("tags:", ", ".join(tags.values()))
    print()
    print(body_md)
    print()

    for comment in comments:
        print(f"{comment['author']} ({comment['email']}) on {comment['date']}:")
        print(comment['comment'])
        print()
    """
    
    post, created = BlogPost.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title,
            "body_md": body_md,
            "created": created,
            "updated": updated,
        },
    )
    post.save()

    for slug, name in tags.items():
        tag, created = Tag.objects.update_or_create(
            slug=slug,
            defaults={"name": name},
        )
        post.tags.add(tag)
        
    post.save()

