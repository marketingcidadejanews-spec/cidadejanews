<?php get_header(); ?>

<main id="content" class="site-main">
    <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
        <article class="post-card" style="padding: 0; overflow: hidden;">
            <?php if ( has_post_thumbnail() ) : ?>
                <?php the_post_thumbnail( 'large', array( 'style' => 'width:100%;height:auto;' ) ); ?>
            <?php endif; ?>
            <div style="padding: 24px;">
                <h1 style="color:#003b82; margin-top:0;"><?php the_title(); ?></h1>
                <p style="color:#6b7280; font-size:13px; margin-bottom:16px;">Publicado em <?php echo esc_html( get_the_date() ); ?></p>
                <?php the_content(); ?>
            </div>
        </article>
    <?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
