#!/usr/bin/python

import cherrypy
from jinja2 import Environment, FileSystemLoader
from imgurpython import ImgurClient
import pymongo
from bson.objectid import ObjectId
import config, config2

#Mongo Stuff
client = pymongo.MongoClient()
env = Environment(loader=FileSystemLoader('templates'))
db = client['jaxtory']
stories = db['stories']
#storyList = list(stories.find({"jType": "story"}))

#Imgur Stuff
iclient = ImgurClient(config.imgur_app, config.imgur_secret, config.imgur_token,config.imgur_rtoken)

class Jaxtory:
    @cherrypy.expose(['m', 'mobile'])
    def index(self):
        return 'Hello'

class Admin:

    @cherrypy.expose()
    def index(self):
        return adminRender()

    @cherrypy.expose()
    def story(self, id):
        return storyRender(id)

    @cherrypy.expose()
    def addStory(self, name=''):
        newStory = {}
        newStory['jType'] = 'story'
        newStory['name'] = name
        stories.insert(newStory)
        return adminRender()

    @cherrypy.expose()
    def remStory(self, id):
        stories.delete_one({"_id": ObjectId(id)})
        return adminRender()

    @cherrypy.expose()
    def addPage(self, storyID, file):
        imconf = {'album': config.album, 'name': file.filename, 'title': file.filename}
        f = open('/tmp/' + file.filename, 'w')
        f.write(file.file.read())

        f.close()
        page = iclient.upload_from_path(f.name, config=imconf, anon=False)
        newPage = {}
        newPage['jType'] = 'page'
        newPage['storyID'] = storyID
        newPage['name'] = page['title']
        newPage['contributers'] = ''
        newPage['desc'] = ''
        newPage['url'] = page['link']
        newPage['thumb'] = page['link'].replace('.jpg','t.jpg').replace('.png','t.jpg').replace('.gif','t.gif')
        newPage['deletehash'] = page['deletehash']
        stories.insert_one(newPage)
        return storyRender(storyID)

    @cherrypy.expose()
    def editPage(self, storyID, pageID, name, contributers, desc):
        newPage = stories.update_one(
            {'_id': ObjectId(pageID)},
            {
                '$set': {
                    'name': name,
                    'contributers': contributers,
                    'desc': desc
                }
            }
        )
        return storyRender(storyID)

    @cherrypy.expose()
    def remPage(self, id, storyID, deletehash):
        stories.delete_one({"_id": ObjectId(id)})

        try:
            iclient.delete_image(deletehash)
        except:
            print("Issue with imgur deletion")
            pass

        return storyRender(storyID)

    @cherrypy.expose()
    def setDefault(self, id):
        defaultStory = stories.find_one({'jType': 'defaultStory'})
        if defaultStory == None:
            newDefault = {}
            newDefault['jType'] = 'defaultStory'
            newDefault['storyID'] = id
            defaultStory = stories.insert_one(newDefault)
        else:
            defaultStory = stories.update_one(
                {'jType': 'defaultStory'},
                {
                    '$set': {
                        'storyID': id
                        }
                }
            )
        return adminRender()

def adminRender():
    baseurl = cherrypy.request.base + cherrypy.request.script_name
    storyList = list(stories.find({"jType": "story"}))
    admin_tmpl = env.get_template('admin.html')
    defaultStory = stories.find_one({'jType': 'defaultStory'})
    return admin_tmpl.render(storyList=storyList, baseurl=baseurl, defaultStory=defaultStory)

def storyRender(id):
    baseurl = cherrypy.request.base + cherrypy.request.script_name
    story = stories.find_one({"_id": ObjectId(id)})
    pageList = list(stories.find({"jType": "page", "storyID": id}).sort("name", pymongo.ASCENDING))
    admin_tmpl = env.get_template('story.html')
    return admin_tmpl.render(pageList=pageList, baseurl=baseurl, story=story)

cherrypy.config.update("server.conf")
cherrypy.tree.mount(Jaxtory(), '/', config2.conf)
cherrypy.tree.mount(Admin(), '/admin', config.conf)

cherrypy.engine.start()
cherrypy.engine.block()
