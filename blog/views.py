from django.shortcuts import render
from blog.models import Comment, Post, Tag


def serialize_post_optimized(post):
    return {
        "title": post.title,
        "teaser_text": post.text[:200],
        "author": post.author.username,
        "comments_amount": post.comments_count,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": post.tags.all(),
        "first_tag_title": post.tags.first().title,
    }


def serialize_tag_optimized(tag):
    return {
        "title": tag.title,
        "posts_with_tag": tag.posts_count,
    }


def index(request):
    most_popular_posts = Post.objects.popular().with_comments_count()[:5]
    most_fresh_posts = Post.objects.fresh().with_comments_count()[:5]
    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        "most_popular_posts": [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
        "page_posts": [serialize_post_optimized(post) for post in most_fresh_posts],
        "popular_tags": [serialize_tag_optimized(tag) for tag in most_popular_tags],
    }
    return render(request, "index.html", context)


def post_detail(request, slug):
    post = Post.objects.select_related("author").get(slug=slug)
    comments = post.comments.prefetch_related("author")

    serialized_comments = []
    for comment in comments:
        serialized_comments.append(
            {
                "text": comment.text,
                "published_at": comment.published_at,
                "author": comment.author.username,
            }
        )

    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": serialized_comments,
        "likes_amount": post.likes.count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": post.tags.all(),
    }

    most_popular_posts = Post.objects.popular().with_comments_count()[:5]
    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        "post": serialized_post,
        "popular_tags": [serialize_tag_optimized(tag) for tag in most_popular_tags],
        "most_popular_posts": [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
    }
    return render(request, "post-details.html", context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)

    most_popular_posts = Post.objects.popular().with_comments_count()[:5]
    most_popular_tags = Tag.objects.popular()[:5]

    related_posts = tag.posts.popular().with_comments_count()[:20]

    context = {
        "tag": tag.title,
        "popular_tags": [serialize_tag_optimized(tag) for tag in most_popular_tags],
        "posts": [serialize_post_optimized(post) for post in related_posts],
        "most_popular_posts": [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
    }
    return render(request, "posts-list.html", context)


def contacts(request):
    # ?????????? ?????????? ?????????? ?????? ?????? ???????????????????? ?????????????? ???? ?????? ????????????????
    # ?? ?????? ???????????? ??????????????
    return render(request, "contacts.html", {})
