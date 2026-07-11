<?php

add_theme_support( 'title-tag' );
add_theme_support( 'post-thumbnails' );
add_theme_support( 'editor-styles' );
add_theme_support( 'align-wide' );
add_theme_support( 'wp-block-styles' );
add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );

function cidade_ja_news_enqueue_assets() {
    wp_enqueue_style( 'cidade-ja-news-style', get_stylesheet_uri(), array(), '1.0.0' );
}
add_action( 'wp_enqueue_scripts', 'cidade_ja_news_enqueue_assets' );

function cidade_ja_news_excerpt_length( $length ) {
    return 22;
}
add_filter( 'excerpt_length', 'cidade_ja_news_excerpt_length', 999 );

function cidade_ja_news_excerpt_more( $more ) {
    return '…';
}
add_filter( 'excerpt_more', 'cidade_ja_news_excerpt_more' );
