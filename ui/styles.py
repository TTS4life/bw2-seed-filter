from tkinter import ttk

def configure_app_styles():
    """Configure consistent styles for the entire application"""
    style = ttk.Style()
    
    # Available themes: 'clam', 'alt', 'default', 'classic'
    # 'clam' is usually the most customizable
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    
    # Configure colors for DARK MODE
    COLORS = {
        'bg': '#2d2d2d',              # Dark gray background
        'fg': '#ffffff',               # White text
        'select_bg': '#4a7a9c',        # Kept same for selection highlight
        'select_fg': '#ffffff',         # White text on selection
        'border': '#555555',            # Medium gray borders
        'error': '#ff6b6b',             # Softer red for errors
        'success': '#51cf66',           # Softer green for success
        'primary': '#4a7a9c',           # Kept same primary color
        'primary_light': '#6b9cbe',      # Lighter version
        'primary_dark': '#2a5a7c',       # Darker version
        'secondary_bg': '#3d3d3d',       # Lighter dark for frames
        'input_bg': '#3d3d3d',           # Background for input fields
        'input_fg': '#ffffff',           # White text in inputs
        'disabled_fg': '#888888',        # Gray for disabled text
        'disabled_bg': '#3d3d3d',        # Background for disabled items
        'hover_bg': '#4d4d4d',           # Hover background
    }
    
    # Configure fonts
    FONTS = {
        'heading': ('Arial', 14, 'bold'),
        'subheading': ('Arial', 12, 'bold'),
        'label': ('Arial', 10),
        'entry': ('Arial', 10),
        'button': ('Arial', 10),
        'small': ('Arial', 9),
    }
    
    # Configure ttk styles with dark mode colors
    
    # Main window style
    style.configure('Main.TFrame', background=COLORS['bg'])
    style.configure('Main.TLabel', background=COLORS['bg'], foreground=COLORS['fg'], font=FONTS['label'])
    
    # Heading styles
    style.configure('Heading.TLabel', font=FONTS['heading'], background=COLORS['bg'], foreground=COLORS['fg'])
    style.configure('Subheading.TLabel', font=FONTS['subheading'], background=COLORS['bg'], foreground=COLORS['fg'])
    
    # Entry style
    style.configure('Form.TEntry', 
                   fieldbackground=COLORS['input_bg'], 
                   foreground=COLORS['input_fg'], 
                   font=FONTS['entry'])
    style.map('Form.TEntry',
              fieldbackground=[('disabled', COLORS['disabled_bg']), ('focus', COLORS['input_bg'])],
              foreground=[('disabled', COLORS['disabled_fg'])])
    
    # Combobox style
    style.configure('Form.TCombobox', 
                   fieldbackground=COLORS['input_bg'], 
                   foreground=COLORS['input_fg'], 
                   font=FONTS['entry'])
    style.map('Form.TCombobox',
              fieldbackground=[('readonly', COLORS['input_bg']), ('disabled', COLORS['disabled_bg'])],
              foreground=[('disabled', COLORS['disabled_fg'])])
    
    # Checkbutton style
    style.configure('Form.TCheckbutton', 
                   background=COLORS['bg'], 
                   foreground=COLORS['fg'], 
                   font=FONTS['label'])
    
    # Button styles
    style.configure('Primary.TButton',
                   font=FONTS['button'],
                   background=COLORS['primary'],
                   foreground=COLORS['fg'],
                   borderwidth=0,
                   focusthickness=3,
                   focuscolor='none')
    style.map('Primary.TButton',
              background=[('active', COLORS['primary_light']),
                         ('pressed', COLORS['primary_dark']),
                         ('disabled', COLORS['disabled_bg'])],
              foreground=[('disabled', COLORS['disabled_fg'])])
    
    style.configure('Secondary.TButton',
                   font=FONTS['button'],
                   background=COLORS['secondary_bg'],
                   foreground=COLORS['fg'],
                   borderwidth=0,
                   focusthickness=3,
                   focuscolor='none')
    style.map('Secondary.TButton',
              background=[('active', COLORS['hover_bg']),
                         ('pressed', COLORS['bg']),
                         ('disabled', COLORS['disabled_bg'])],
              foreground=[('disabled', COLORS['disabled_fg'])])
    
    # LabelFrame style
    style.configure('Form.TLabelframe',
                   background=COLORS['bg'],
                   foreground=COLORS['fg'],
                   relief='solid',
                   borderwidth=1)
    style.configure('Form.TLabelframe.Label',
                   font=FONTS['subheading'],
                   background=COLORS['bg'],
                   foreground=COLORS['fg'])
    
    # Separator style
    style.configure('Form.TSeparator', background=COLORS['border'])
    
    # Error and success styles
    style.configure('Error.TLabel', 
                   foreground=COLORS['error'], 
                   font=FONTS['small'], 
                   background=COLORS['bg'])
    style.configure('Success.TLabel', 
                   foreground=COLORS['success'], 
                   font=FONTS['small'], 
                   background=COLORS['bg'])
    
    return style, COLORS, FONTS