<?php get_header(); ?>

<main id="content" class="site-main">
    <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <h2><?php the_title(); ?></h2>
            <?php the_content(); ?>
        </article>
    <?php endwhile; else : ?>
        <p>Nenhum conteúdo encontrado.</p>
    <?php endif; ?>
</main>

<?php get_footer(); ?>
