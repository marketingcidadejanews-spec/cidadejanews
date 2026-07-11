<?php get_header(); ?>

<main id="content" class="site-main">
    <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
        <article class="post-card" style="padding: 24px;">
            <h1 style="color:#003b82; margin-top:0;"><?php the_title(); ?></h1>
            <?php the_content(); ?>
        </article>
    <?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
