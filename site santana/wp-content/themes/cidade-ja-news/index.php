<?php get_header(); ?>

<main id="content" class="site-main">
    <section class="hero-editorial" id="editorial">
        <span class="categoria">CIDADE JÁ NEWS</span>
        <h1>Um portal editorial para notícias, cultura e informação da Bahia.</h1>
        <p>Este tema foi preparado com estrutura de blog e blocos modulares para facilitar a edição no Elementor e no editor de blocos do WordPress.</p>
        <a class="hero-cta" href="#ultimas">Ver últimas notícias</a>
    </section>

    <section id="ultimas">
        <h2 class="section-title">Últimas notícias</h2>
        <div class="post-grid">
            <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class( 'post-card' ); ?>>
                    <?php if ( has_post_thumbnail() ) : ?>
                        <a href="<?php the_permalink(); ?>">
                            <?php the_post_thumbnail( 'large' ); ?>
                        </a>
                    <?php endif; ?>
                    <div class="post-card__body">
                        <div class="post-card__meta">
                            <?php echo esc_html( get_the_date() ); ?>
                        </div>
                        <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
                        <p><?php echo esc_html( wp_strip_all_tags( get_the_excerpt() ) ); ?></p>
                        <a href="<?php the_permalink(); ?>">Ler notícia →</a>
                    </div>
                </article>
            <?php endwhile; else : ?>
                <p>Nenhum conteúdo encontrado.</p>
            <?php endif; ?>
        </div>
    </section>
</main>

<?php get_footer(); ?>
