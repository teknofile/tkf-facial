<?php
/*
Plugin Name: tkf-facial
Version: 0.0.1
Description: This plugin provides an interface into facial recognition capabilities
Plugin URI: https://github.com/teknofile/tkf-facial
Author: teknofile
Author URI: https://blog.teknofile.space
*/

/** 
 * This is the main file of the plugin, called by Piwigo in "include/common.inc.php". At this 
 * point of the code, Piwigo is not completely initialized, so nothing should be done directly
 * except define constants and event handlers (see http://piwigo.org/doc/doku.php?id-dev:plugins)
 */

 defined('PHPWG_ROOT_PATH') or die('Hacking attempt!');

 // +--------------------------------------------------------------+
 // | Define Plugin Constants                                      |
 // +--------------------------------------------------------------+

 global $prefixeTable;

 define('TKF_FACIAL_ID',        basename(dirname(__FILE__)));
 define('TKF_FACIAL_PATH',      PHPWG_PLUGINS_APTH . basename(dirname(__FILE__)) . '/');

 // Hook on to an event to show the administration page.
 add_event_handler('get_admin_plugin_menu_links', 'facial_admin_menu');

 function facial_admin_menu($menu) {
    array_push(
         $menu,
         array(
             'NAME' => 'Facial',
             'URL'  => get_admin_plugin_menu_link(dirname(__FILE__)) . '/admin.php'
         )
    );

    return $menu
 }
 ?>