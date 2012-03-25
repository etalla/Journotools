/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
	{
		// Define changes to default configuration here. For example:
		// config.language = 'fr';
		// config.uiColor = '#AADC6E';

		// YOU CAN CREATE SEVERAL TOOLBAR SETTINGS BY NAMING THEM... SEE http://docs.cksource.com/CKEditor_3.x/Developers_Guide/Toolbar FOR MORE INFO.
		
		config.toolbar= 
		[
			{ name: 'tools', items : [ 'Maximize' ] },
			{ name: 'document', items : ['Preview','Print'] },
			{ name: 'styles', items : [ 'Font','FontSize','Styles','Format' ] },
			{ name: 'colors', items : [ 'TextColor','BGColor' ] },
			{ name: 'basicstyles', items : [ 'Bold','Italic','Strike','-','RemoveFormat' ] },
			// Insert breaks between toolbars: '/',
			{ name: 'clipboard', items : [ 'Undo','Redo', 'Cut','Copy','Paste','PasteText','-' ] },
			{ name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','Scayt' ] },
			{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote' ] },
			{ name: 'insert', items : [ 'Image','Table','HorizontalRule','SpecialChar','PageBreak','Iframe' ] },		
			{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
		];
	};

