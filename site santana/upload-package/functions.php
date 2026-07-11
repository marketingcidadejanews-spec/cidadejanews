<?php

add_theme_support( 'title-tag' );
add_theme_support( 'post-thumbnails' );
add_theme_support( 'editor-styles' );
add_theme_support( 'align-wide' );
add_theme_support( 'wp-block-styles' );

function cidade_ja_news_enqueue_assets() {
    wp_enqueue_style( 'cidade-ja-news-style', get_stylesheet_uri(), array(), '1.0.0' );
}
add_action( 'wp_enqueue_scripts', 'cidade_ja_news_enqueue_assets' );
