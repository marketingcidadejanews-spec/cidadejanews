<?php get_header(); ?>

<main id="content" class="site-main">
    <h1 class="section-title">Arquivos</h1>
    <div class="post-grid">
        <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
            <article class="post-card">
                <?php if ( has_post_thumbnail() ) : ?>
                    <a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'large' ); ?></a>
                <?php endif; ?>
                <div class="post-card__body">
                    <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
                    <p><?php echo esc_html( wp_strip_all_tags( get_the_excerpt() ) ); ?></p>
                </div>
            </article>
        <?php endwhile; endif; ?>
    </div>
</main>

<?php get_footer(); ?>
