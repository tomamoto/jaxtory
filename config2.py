import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

conf = {
   '/style.css': {
       'tools.staticfile.on': True,
       'tools.staticfile.filename': os.path.join(current_dir, 'static') + '/style.css'
   }
}
