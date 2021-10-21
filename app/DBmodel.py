from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from flask import current_app
from werkzeug.security import generate_password_hash
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import scale, rotate
import os
import shutil
import click
import json
import random

db = SQLAlchemy()

class User(db.Model):
    """
    Class to handle users and user associated data

    Attributes:
       username
       password
       email (not used in right now)
       access_level: controls which parts of the APP the user can access
       created
       studies: links to all studies the user created
       results: links to results the user produced
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(60))
    access_level = db.Column(db.Integer(), nullable=False)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    studies = db.relationship("Study", backref="user", lazy=True,
                              cascade="all, delete-orphan")
    results = db.relationship("Result", backref="user", lazy=True,
                              cascade="all, delete-orphan")

    def is_user(self):
        return self.access_level == 1

    def is_study_admin(self):
        return self.access_level == 2

    def is_user_admin(self):
        return self.access_level == 3

#tables for m to n relationships (study - images)
study_images = db.Table("study_images",
    db.Column("study_id",db.Integer, db.ForeignKey("study.id"), primary_key=True),
    db.Column("image_id",db.Integer, db.ForeignKey("image.id"), primary_key=True)
)

class Study(db.Model):
    """
    Class to handle studies created with HON

    Attributes:
       created
       updated (not working right now)
       title
       password
       created
       description
       design: links to the design used
       imgsets: links to the associated sets of images
    """
    __table_args__ = (db.UniqueConstraint("title","user_id", name = "title_id"),)
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    updated = db.Column(db.DateTime(), server_default=db.func.now(),
                        server_onupdate=db.func.now())
    title = db.Column(db.String(120),unique=False)
    password = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    design = db.relationship("Design", backref="study", lazy=True, uselist=False,
                             cascade="all, delete-orphan")
    images = db.relationship("Image",secondary=study_images, backref=db.backref("studies", lazy=True),lazy='subquery')
    imgsets = db.relationship("Imgset", backref="study", lazy=True, order_by="Imgset.position",
                              cascade="all, delete-orphan")
    user_study_progress = db.relationship("User_study_progress", backref="study",
                                           lazy=True, cascade="all, delete-orphan")

    def get_cs_stack_by_imageIds(self, image_ids):
        cs_stack = {"imageIds":[],
                    "currentImageIdIndex":0}
        images = [image for image in self.images if image.id in image_ids]
        images.sort(key=lambda image: image.name)
        for image in images:
            url = os.path.join(image.base_url,image.name)
            if ".dcm" in image.name:
                url = "wadouri:" + url
            cs_stack["imageIds"].append(url)
        return cs_stack

    def images_to_cs_stacks(self,group_info):
        cs_stacks = {}
        self.images.sort(key=lambda image: image.name)
        for image in self.images:
            url = os.path.join(image.base_url,image.name)
            if ".dcm" in image.name:
                url = "wadouri:" + url

            if group_info != "single_images":
                stack_name = "_".join(image.name.split("_")[0:3])
            else:
                stack_name = image.name

            if stack_name in cs_stacks:
                cs_stacks[stack_name]["image_ids"] += "-"+str(image.id)
                cs_stacks[stack_name]["imageIds"].append(url)
            else:
                cs_stacks[stack_name] = {"name":stack_name,
                                         "image_ids":str(image.id),
                                         "imageIds":[url]}

        cs_stacks = [cs_stacks[cs_stack] for cs_stack in cs_stacks]
        return cs_stacks



    def insert_imgset(self,imgset,position):
        self.imgsets.insert(position,imgset)
        # updating position
        for imgset in self.imgsets:
            imgset.position = self.imgsets.index(imgset)
        db.session.commit()


    def shuffle_imgsets(self):
        # copy to dict otherwise constraint issues
        imgsets = []
        for imgset in self.imgsets:
            imgsets.append(imgset.to_dict())
            db.session.delete(imgset)
        db.session.commit()
        random.shuffle(imgsets)
        for i, imgset in enumerate(imgsets):
            imgset_new = Imgset(study_id=imgset["study_id"],
                                position=i)
            for image in imgset["images"]:
                image = Image_stack(div_id=image["div_id"],
                            url=json.dumps(image["url"]),
                            viewport=json.dumps(image["viewport"]))
                imgset_new.images.append(image)

            db.session.add(imgset_new)

        db.session.commit()

    def get_image_dir(self):
        path = os.path.join(current_app.config["IMAGE_PATH"],str(self.user_id),str(self.id))
        return path

    def update_imgset_pos(self):
        for imgset in self.imgsets:
            imgset.position = self.imgsets.index(imgset)
        db.session.commit()


class Design(db.Model):
    """
    Class to handle studies designs created with HON

    Attributes:
       instructions
       button_labels
       background_color
       text_color
       numb_img
       numb_refimg
       numb_rois: idea was to limit the number of rois the user can mark (not  implemented)
       show_viewport_info
       transition_time: time the display remains dark between two img sets
       tools: links to the tools used
       scales: links to the scales used
    """
    id = db.Column(db.Integer(), primary_key=True)
    study_id = db.Column(db.Integer(), db.ForeignKey("study.id"), nullable=False)
    instructions = db.Column(db.String(2000))
    button_labels = db.Column(db.String(120))
    background_color = db.Column(db.String(120))
    text_color = db.Column(db.String(120))
    numb_img = db.Column(db.Integer())
    numb_refimg = db.Column(db.Integer())
    img_width = db.Column(db.Integer())
    img_height = db.Column(db.Integer())
    numb_rois = db.Column(db.Integer())
    show_viewport_info = db.Column(db.Boolean)
    transition_time = db.Column(db.Integer())
    randomize_order = db.Column(db.Boolean)
    scales = db.relationship("Scale", lazy=True, cascade="all, delete-orphan")
    tools = db.relationship("Tool", lazy=True, cascade="all, delete-orphan")


    def get_defaults(self):
        """
        helper function to define the default study design

        Returns:
            nothing
            just updates the design attributes and fill them with defined defaults
        """
        self.instructions=""
        self.button_labels="Next"
        self.background_color="black"
        self.text_color="white"
        self.numb_img=2
        self.numb_refimg=1
        self.img_width=512
        self.img_height=512
        self.numb_rois=None
        self.show_viewport_info=False
        self.transition_time=0
        self.tools=[]
        self.scales=[]


class Scale(db.Model):
    """
    Class to handle scales (numerical) associated with a design created with HON

    Attributes:
       min: smallest number of the scale
       max: largest number of the scale
       text: description of scale
    """
    id = db.Column(db.Integer(), primary_key=True)
    design_id = db.Column(db.Integer(), db.ForeignKey("design.id"), nullable=False)
    min = db.Column(db.Integer())
    max = db.Column(db.Integer())
    text = db.Column(db.String(1000))
    type = db.Column(db.String(20))


class Tool(db.Model):
    """
    Class to handle tools associated with a design created with HON

    Attributes:
       cs_name: toolname in cornerstone tools
       label: tool name show to the user
       key_binding: hot key to actiavte tool
       status: track if the tool should be available for the study participant
       settings: save tool setting like (mouse key to use tool, not used right now)
    """
    __table_args__ = (db.UniqueConstraint("design_id","cs_name", name = "unique_set"),)
    id = db.Column(db.Integer(), primary_key=True)
    design_id = db.Column(db.Integer(), db.ForeignKey("design.id"), nullable=False)
    cs_name = db.Column(db.String(120))
    label = db.Column(db.String(120))
    key_binding = db.Column(db.String(120))
    status = db.Column(db.String(120))
    settings = db.Column(db.String(120))


class Result(db.Model):
    """
    Class to handle result from a study created with HON

    Attributes:
       stack_picked
       imgset: links to the imgset shown
       created
       scale_input
    """
    __table_args__ = (db.UniqueConstraint("user_id","imgset_id", name = "unique_result"),)
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    study_id = db.Column(db.Integer(), db.ForeignKey("study.id"), nullable=False)
    imgset_id = db.Column(db.Integer(),db.ForeignKey("imgset.id"), nullable=False)
    stack_picked = db.relationship("Image_stack", backref="result", lazy=False,
                                   cascade="all, delete-orphan", uselist=False)
    imgset = db.relationship("Imgset", backref="result", lazy=False, uselist=False)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    scale_input = db.Column(db.String(1000))


    def to_dict(self):
            result_dict = {}
            result_dict["id"] = self.id
            result_dict["user_id"] = self.user_id
            result_dict["study_id"] = self.study_id
            result_dict["imgset_id"] = self.imgset_id
            result_dict["stack_picked"] = self.stack_picked.to_dict()
            result_dict["created"] = self.created
            result_dict["scale_input"] = self.scale_input

            return result_dict



class User_study_progress(db.Model):
    """
    Class to keep track of the study progress for each user and study

    Attributes:
       user:
       imgset:
       updated:
    """
    __table_args__ = (db.UniqueConstraint("user_id","study_id", name = "study_progress"),)
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="user_study_progress", lazy=True, uselist=False)
    study_id = db.Column(db.Integer(), db.ForeignKey("study.id"), nullable=False)
    imgset_id = db.Column(db.Integer(),db.ForeignKey("imgset.id"),nullable=False)
    imgset = db.relationship("Imgset", backref="user_study_progress", lazy=True, uselist=False)
    updated = db.Column(db.DateTime(), server_default=db.func.now(),
                        server_onupdate=db.func.now())


class Imgset(db.Model):
    """
    Class to save imgsets used with HON

    Attributes:
       position:
       image_stacks:
       results:
    """
    #__table_args__ = (db.UniqueConstraint("study_id","position", name = "imgset_id"),)
    id = db.Column(db.Integer(), primary_key=True)
    study_id = db.Column(db.Integer(), db.ForeignKey("study.id"), nullable=False)
    position = db.Column(db.Integer(), nullable=False)
    image_stacks = db.relationship("Image_stack", lazy=False, cascade="all, delete-orphan")
    results = db.relationship("Result", lazy=True, cascade="all, delete-orphan")


    def get_stack_by_div_id(self,div_id):
        stack = [stack for stack in self.image_stacks if stack.div_id == div_id]
        if len(stack) == 1:
            stack = stack[0]
        else:
            stack = None
        return stack


    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["study_id"] = self.study_id
        dict["position"] = self.position
        dict["image_stacks"] = []
        for stack in self.image_stacks:
            dict["image_stacks"].append(stack.to_dict())

        return dict


class Image(db.Model):
    """
    Class to keep track of image files associated with a study

    Attributes:
       url:
    """
    id = db.Column(db.Integer(), primary_key=True)
    base_url = db.Column(db.String(1000))
    name = db.Column(db.String(120))

#table for m to n relationships (image_stacks - images)
stack_images = db.Table("stack_images",
    db.Column("image_stack_id",db.Integer, db.ForeignKey("image_stack.id"), primary_key=True),
    db.Column("image_id",db.Integer, db.ForeignKey("image.id"), primary_key=True)
)


class Image_stack(db.Model):
    """
    Class to save image configurations used by HON
    linked to imgset

    Attributes:
       div_id:
       url:
       viewport:
       tool_state:
    """
    __table_args__ = (db.UniqueConstraint("imgset_id","result_id","div_id"),
                      db.CheckConstraint('(imgset_id IS NULL) <> (result_id IS NULL)'),)
    id = db.Column(db.Integer(), primary_key=True)
    # image either belongs to a result or an imgset
    imgset_id = db.Column(db.Integer(), db.ForeignKey("imgset.id"))
    result_id = db.Column(db.Integer(), db.ForeignKey("result.id"))
    div_id = db.Column(db.String(120))
    name = db.Column(db.String(120))
    images = db.relationship("Image",secondary=stack_images, backref=db.backref("image_stacks", lazy=True),lazy='subquery')
    viewport = db.Column(db.String(1000))
    tool_state = db.Column(db.Text())

    def to_dict(self):
        image_stack_dict = {}
        image_stack_dict["div_id"] = self.div_id
        #dict["base_url"] = self.base_url
        image_stack_dict["name"] = self.name
        #dict["image_names"] = json.loads(self.image_names)
        imageIds = ['wadouri:' + image.base_url + image.name if ".dcm" in  image.name else image.base_url + "/" + image.name for image in self.images]
        image_stack_dict["cs_stack"] = {"imageIds":imageIds,
                            "currentImageIdIndex":0}
        if self.viewport:
            image_stack_dict["viewport"] = json.loads(self.viewport)
        if self.tool_state:
            image_stack_dict["tool_state"] = json.loads(self.tool_state)

        return image_stack_dict


    def get_filenames(self):
        image_names = json.loads(self.image_names)
        return image_names


class Annotations:
    """
    Class to handle annotation data (rois) collected with cornerstone tools (javascript library)

    Args:
       tool_state (str in json format)

    Attributes:
       annotations (dict): stores the toolstate data
    """
    def __init__(self,tool_state):
        self.annotations = tool_state
        self.set_polygons()

    def get_tool_state_string(self):
        return(json.dumps(self.annotations))

    def get_tool_coordinates(self):
        coordinates = []
        for ann in self.annotations["data"]:
            coordinates.append(ann["handles"])
        return(coordinates)

class Length(Annotations):
        def set_polygons(self):
            self.lines = []
            """
                generate shapley linestrings from annotation data and store them
            """
            for ann in self.annotations["data"]:
                start_x = ann["handles"]["start"]["x"]
                end_x = ann["handles"]["end"]["x"]
                start_y = ann["handles"]["start"]["y"]
                end_y = ann["handles"]["end"]["y"]
                line = LineString([(start_x,start_y),(end_x,end_y)])
                self.lines.append(line)

class Rois(Annotations):
    def calc_seq_metric(self,rois_gt,metric):
        results = []
        for polygon in self.polygons:
            for polygon_gt in rois_gt.polygons:
                result = eval(metric + "(polygon , polygon_gt)")
                result = round(result,2)
                results.append(result)
        return(results)


class EllipticalRoi(Rois):
    def set_polygons(self):
        self.polygons = []
        """
            generate shapley polygons from annotation data and store them
        """
        for ann in self.annotations["data"]:
            width = abs(ann["handles"]["end"]["x"] - ann["handles"]["start"]["x"])
            height = abs(ann["handles"]["end"]["y"] - ann["handles"]["start"]["y"])
            center_x = (ann["handles"]["end"]["x"] + ann["handles"]["start"]["x"])/2
            center_y = (ann["handles"]["end"]["y"] + ann["handles"]["start"]["y"])/2
            ellipsis = create_ellipse((center_x,center_y),width,height)
            self.polygons.append(ellipsis)

class RectangleRoi(Rois):
     def set_polygons(self):
        self.polygons = []
        """
            generate shapley polygons from annotation data and store them
        """
        for ann in self.annotations["data"]:
            start_x = ann["handles"]["start"]["x"]
            end_x = ann["handles"]["end"]["x"]
            start_y = ann["handles"]["start"]["y"]
            end_y = ann["handles"]["end"]["y"]
            center_x = (ann["handles"]["end"]["x"] + ann["handles"]["start"]["x"])/2
            center_y = (ann["handles"]["end"]["y"] + ann["handles"]["start"]["y"])/2
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)
            rectangle = Polygon([(center_x - width/2, center_y + height/2),
                                 (center_x + width/2, center_y + height/2),
                                 (center_x + width/2, center_y - height/2),
                                 (center_x - width/2, center_y - height/2)])
            self.polygons.append(rectangle)

class FreehandRoi(Rois):
    def set_polygons(self):
        self.polygons = []
        """
            generate shapley polygons from annotation data and store them
        """
        for ann in self.annotations["data"]:
            points = []
            for point in ann["handles"]["points"]:
                points.append(Point(point["x"],point["y"]))
            polygon = Polygon(points)
            self.polygons.append(polygon)


def iou(polygon_1,polygon_2):
        """
        Calculate intercept over union for shapely polygons.

        Args:
            polygon_1
            polygon_2

        Returns:
            intercept over union

        """
        area_intersection = polygon_1.intersection(polygon_2).area
        area_polygon_1_polygon_2 = polygon_1.union(polygon_2).area
        iou = area_intersection/(area_polygon_1_polygon_2) * 100
        return(iou)

def dice(polygon_1,polygon_2):
        """
        Calculate intercept dice for shapely polygons.

        Args:
            polygon_1
            polygon_2

        Returns:
            intercept over union

        """
        area_intersection = polygon_1.intersection(polygon_2).area
        area_polygon_1_polygon_2 = polygon_1.union(polygon_2).area
        dice = (2*area_intersection)/(polygon_1.area + polygon_2.area) * 100
        return(dice)

def perc_correct_pixels(polygon_1,polygon_2):
        """
        Calculate area percentage of a shapely polygon
        intercepting with another polygon.

        Args:
            polygon_1
            polygon_2

        Returns:
            percentage intercepting

        """
        area_intersection = polygon_1.intersection(polygon_2).area
        try:
            perc_intersect = area_intersection/polygon_1.area * 100
            return(perc_intersect)
        except:
            return -1

def create_ellipse(center,width,height,angle=0):
    """
    Generate an ellipse using shapely. For more information see:
    https://gis.stackexchange.com/questions/243459/drawing-ellipse-with-shapely

    Args:
        center (double)
        width (double)
        height (double)
        angle (double)

    Returns:
        shapely polygon object

    """
    center = Point(center)
    circle = center.buffer(1)
    ellipse = scale(circle,(width/2),(height/2))
    ellipse = rotate(ellipse,angle)
    return(ellipse)

def init_db():
    # create db
    db.drop_all()
    db.create_all()
    click.echo("Initialized the database.")

def init_img_dir():
    #create folders for study images
    image_folder = current_app.config["IMAGE_PATH"]
    if os.path.isdir(image_folder):
        shutil.rmtree(image_folder)
    os.mkdir(image_folder)
    click.echo("Initialized folders for images.")

#needed for tests etc
def init_default_users():
    #test users
    users = [("user","user",1),("sadmin","sadmin",2),("uadmin","uadmin",3)]
    for username,password,access_level in users:
        user = User(username=username,
                    password=generate_password_hash(password),
                    access_level=access_level)
        db.session.add(user)
        click.echo(username + " added. Username:" + username + " Password:" + password + "." )
    db.session.commit()
    os.mkdir(os.path.join(current_app.config["IMAGE_PATH"],"2"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    init_img_dir()
    init_default_users()

@click.command("change-base-url-command")
@click.option('--config')
@with_appcontext
def change_base_url_command():
    images = Image.query.all()
    for image in images:
        image.base_url = image.base_url.replace("http://127.0.0.1:5000/","https://phantomx.pythonanywhere.com/")
    db.session.commit()