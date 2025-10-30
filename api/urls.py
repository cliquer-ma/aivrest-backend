from django.urls import path

from api.views import (
    ChatsView,
    ChatView,
    ChatHistoryView,

    ProgramsView,
    ProgramsTypesView,
    ProgramView,

    PostsView,
    PostView,
    CreatePostView,
    PostLikesView,
    PostCommentsView,
    TogglePostLikeView,
    CommentPostView,
)

urlpatterns = [
    path('xenon/chats/',                ChatsView.as_view(),                name='api_chats'),
    path('xenon/send/',                 ChatView.as_view(),                 name='api_chat'),
    path('xenon/chat-history/',         ChatHistoryView.as_view(),          name='api_chat_history'),

    path('xenon/programs/',             ProgramsView.as_view(),             name='api_programs'),
    path('xenon/programs-types/',       ProgramsTypesView.as_view(),        name='api_programs_types'),
    path('xenon/program/',              ProgramView.as_view(),              name='api_program'),

    path('radon/posts/',                PostsView.as_view(),                name='api_posts'),
    path('radon/post/',                 PostView.as_view(),                 name='api_post'),
    path('radon/create-post/',          CreatePostView.as_view(),           name='api_create_post'),
    path('radon/post-likes/',           PostLikesView.as_view(),            name='api_post_likes'),
    path('radon/post-comments/',        PostCommentsView.as_view(),         name='api_post_comments'),
    path('radon/toggle-post-like/',     TogglePostLikeView.as_view(),       name='api_toggle_post_like'),
    path('radon/comment-post/',         CommentPostView.as_view(),          name='api_comment_post'),
]

