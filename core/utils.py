import http.client
import json
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO_ID = "R_kgDOTlMmZQ"
CATEGORY_ID = "DIC_kwDOTlMmZc4DCLm2"


def github_graphql(query, variables):
    conn = http.client.HTTPSConnection("api.github.com")
    payload = json.dumps({
        "query": query,
        "variables": variables,
    })
    conn.request(
        "POST",
        "/graphql",
        body=payload,
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
    data = graphql(query, variables)
    return data["data"]["createDiscussion"]["discussion"]["url"]


def get_ids():
    return github_graphql("""
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
""", {})

