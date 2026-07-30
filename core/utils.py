import http.client
import json
import os

from markdown_it import MarkdownIt


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO_ID = "R_kgDOTlMmZQ"
CATEGORY_ID = "DIC_kwDOTlMmZc4DCLm2"

_md = MarkdownIt("commonmark")


def render_markdown(text):
    return _md.render(text)


def _github_graphql(query, variables=None):
    if variables is None:
        variables = {}
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request(
        "POST",
        "/graphql",
        body=json.dumps({"query": query, "variables": variables}),
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "GeekFunkLabs",
        },
    )
    response = conn.getresponse()
    return json.loads(response.read())


def github_create_discussion(post):
    excerpt = post.excerpt or post.body_md[:200]

    variables = {
        "repositoryId": REPO_ID,
        "categoryId": CATEGORY_ID,
        "title": post.title,
        "body": f"""\
> {excerpt}

(Full post at https://geekfunklabs.com/blog/{post.slug})
"""
    }

    query = """
mutation CreateDiscussion($repositoryId: ID!, $categoryId: ID!, $body: String!, $title: String!) {
  createDiscussion(input: {
    repositoryId: $repositoryId,
    categoryId: $categoryId,
    body: $body,
    title: $title
  }) {
    discussion {
      url
    }
  }
}
"""
    data = _github_graphql(query, variables)
    return data["data"]["createDiscussion"]["discussion"]["url"]


def get_ids():
    return _github_graphql("""
query MyQuery {
  repository(name: "geekfunklabs.com", owner: "GeekFunkLabs") {
    id
    discussionCategories(first: 10) {
      edges {
        node {
          id
          name
        }
        cursor
      }
    }
  }
}
""")

