<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the website, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', '' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'a$Q@@bU<.Bgp%zrg|jey VQ) |,=lGLDGYpR2Qg5]=.[Nb-y+Q#X#*W{H5 JkyWV' );
define( 'SECURE_AUTH_KEY',  'VN$GA8R4*%2 ;6qA<h!280c&hyfDT>w75UXY&9JJZDdy6A9@CRYQN,:~a=!fL%4$' );
define( 'LOGGED_IN_KEY',    'A-YTxahx?#*c{9S@/jA|G4oM3OS$_J18#Dr@PS:cf+=ZD/}cxzUqE+:Woi;1Kn>=' );
define( 'NONCE_KEY',        'd@Z<LaoOJLcE,=Wqw!F8vIj9%g%54%6.4m$E@9*Q`QLOdq|:IWZXb$FcK@o|ZC+&' );
define( 'AUTH_SALT',        'A|XM5ZFlimWfnj66Du7#H07$~P8E]:f L)T:?G-d/CxzdjN<Xxl87?rYIUj:OHQe' );
define( 'SECURE_AUTH_SALT', 'n!Dzo6Yp|IhUTl5%2d,<r^{(3,B[09e.cm~Y*{3h3rDj+{U]Uj?Ah36Hw(HZsA_&' );
define( 'LOGGED_IN_SALT',   'Hw4SDj!w{Xyy?8EX_t1;W_A-zX3zqz4]rtm8Y?6nQ)gh,lKRA]1Wu%guj$ /BS@E' );
define( 'NONCE_SALT',       ')pCKQ2W{L+O[tgt 9Be6f@NMJQ-GbbxcjT3@=<0vLb/0 ZY&Ar|w+( J;II7&9#-' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'blog_wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
