<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

<header class="site-header">
    <a class="site-brand" href="<?php echo esc_url( home_url( '/' ) ); ?>">
        <span class="cidade">CIDADE</span>
        <span class="ja">JÁ</span>
        <span class="news">NEWS</span>
    </a>

    <nav class="site-nav" aria-label="Navegação principal">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>">Início</a>
        <a href="#editorial">Editorial</a>
        <a href="#ultimas">Últimas</a>
        <a href="#contato">Contato</a>
    </nav>
</header>
