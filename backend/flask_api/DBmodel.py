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
import pandas as pd
import numpy as np
import nibabel as nib


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
    username = db.Column(db.String(50), unique=True, nullable=False)
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
#to do: to enable image sharing between studies => feature never finished
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
    results = db.relationship("Result", backref="study", lazy=True, cascade="all, delete-orphan")
    user_study_progress = db.relationship("User_study_progress", backref="study",
                                           lazy=True, cascade="all, delete-orphan")

    def to_dict(self,include_images=False, include_imagesets=False):
            study_dict = {}
            study_dict["id"] = self.id
            study_dict["user_id"] = self.user_id
            study_dict["created"] = self.created
            study_dict["updated"] = self.updated
            study_dict["title"] = self.title
            study_dict["password"] = ''
            study_dict["description"] = self.description
            study_dict["design"] = self.design.to_dict()
            if include_images:
                # study_dict["images"] = [image.to_dict() for image in self.images]
                study_dict["stacks"] = self.get_stacks()
            if include_imagesets:
                study_dict["imgsets"] = [imgset.to_dict() for imgset in self.imgsets]
            study_dict["user_study_progress"] = [usp.to_dict() for usp in self.user_study_progress]

            return study_dict


    # def get_cs_stack_by_imageIds(self, image_ids):
    #     cs_stack = {"imageIds":[],
    #                 "currentImageIdIndex":0}
    #     images = [image for image in self.images if image.id in image_ids]
    #     images.sort(key=lambda image: image.name)
    #     for image in images:
    #         url = os.path.join(image.base_url,image.name)
    #         if ".dcm" in image.name:
    #             url = "wadouri:" + url
    #         cs_stack["imageIds"].append(url)
    #     return cs_stack

    # def images_to_cs_stacks(self,group_info="group"):
    #     cs_stacks = {}
    #     self.images.sort(key=lambda image: image.name)
    #     for image in self.images:
    #         url = os.path.join(image.base_url,image.name)
    #         if ".dcm" in image.name:
    #             url = "wadouri:" + url

    #         if group_info != "single_images":
    #             stack_name = "_".join(image.name.split("_")[0:3])
    #         else:
    #             stack_name = image.name

    #         if stack_name in cs_stacks:
    #             cs_stacks[stack_name]["imageIds"].append(url)
    #         else:
    #             cs_stacks[stack_name] = {"name":stack_name,
    #                                      "imageIds":[url],
    #                                      "currentImageIdIndex":0}

    #     cs_stacks = [cs_stacks[cs_stack] for cs_stack in cs_stacks]
    #     return cs_stacks

    def get_stacks(self):
        stacks = []
        image_dir = self.get_image_dir()
        stack_folders = os.listdir(image_dir)
        stack_folders.sort()
        for stack_folder in stack_folders:
            stack_path = os.path.join(image_dir,stack_folder)
            stack = self.get_stack(stack_path)
            stacks.append(stack)

        return stacks

    def get_stack(self, stack_path):
        stack_files = os.listdir(stack_path)
        stack = {}
        stack_folder = os.path.normpath(stack_path).split(os.sep)[-1]
        stack["name"] = stack_folder
        stack["size"] = sum( [os.path.getsize(os.path.join(stack_path, stack_file)) for stack_file in stack_files] ) 
        stack["slices"] = len(stack_files)
        stack["files"] = stack_files
        stack["files"].sort()
        stack["cs_stack"] = {"imageIds":[], "currentImageIdIndex":0}
        images = [image for image in self.images if image.base_url.split(os.sep)[-2] == stack_folder]
        for image in images:
            url = os.path.join(image.base_url,image.name)
            if ".dcm" in image.name.lower():
                url = "wadouri:" + url                
            stack["cs_stack"]["imageIds"].append(url)
        stack["cs_stack"]["imageIds"]
        stack["cs_stack"]["imageIds"].sort()
        return stack

    def insert_imgset(self,imgset,position):
        # add to db
        # db.session.add(imgset)
        # db.session.commit()    
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

    # to do fix and transfer code from studie.py
    def auto_create_imgsets(self, imgset_config):
        image_stacks, ref_stack, error_image_stacks = self.get_image_stacks(imgset_config)

        # create imgsets
        if imgset_config.imgset_type == "afc":
            imgsets,error_imgsets  = self.auto_create_AFC_imgsets(image_stacks,imgset_config)
        elif imgset_config.imgset_type == "standard":
            imgsets,error_imgsets = self.auto_create_ROClike_imgsets(image_stacks, imgset_config)

        return imgsets, ref_stack, error_image_stacks, error_imgsets

    # def get_image_stacks(self,imgset_config):
    #     # build stacks from images
    #     image_stacks = {}
    #     ref_stack = {}
    #     error = None

    #     self.images.sort(key=lambda image: image.name)
    #     for image in self.images:
    #         if imgset_config.stackmode == "single_images":
    #             stack_name = image.name
    #         else:
    #             stack_name = "_".join(image.name.split("_")[0:3])

    #         if stack_name in image_stacks:
    #             image_stacks[stack_name]["images"].append(image)
    #         else:
    #             image_stacks[stack_name] = {}
    #             image_stacks[stack_name]["name"] = stack_name
    #             image_stacks[stack_name]["viewport"] = imgset_config.viewport
    #             image_stacks[stack_name]["images"] = [image]
        
    #     if imgset_config.ref_stack_name in image_stacks.keys():
    #         ref_stack = image_stacks[imgset_config.ref_stack_name]
    #     elif imgset_config.ref_stack_name != "" and imgset_config.ref_stack_name not in image_stacks.keys():
    #         error = "Error creating the reference stack: " + imgset_config.ref_stack_name + "."
    #     elif imgset_config.ref_stack_name == "" and imgset_config.div_ids_ref:
    #         error = "No reference stack specified, but the number of reference images (general settings) is not 0."
    #     image_stacks = [image_stacks[stack_name] for stack_name in image_stacks if stack_name != imgset_config.ref_stack_name]
        
    #     return image_stacks, ref_stack, error

    # def auto_create_AFC_imgsets(self, image_stacks, config):
    #     #auto create imgsets
    #     imgset_size = len(config.div_ids)
    #     error = ""
    #     pos_stacks = []
    #     neg_stacks = []
    #     for stack in image_stacks:
    #         stack_info = stack["name"].split("_")
    #         if len(stack_info) < 3:
    #             error += stack["name"] + ": wrong naming scheme." + "\n"
    #         elif config.pos_pattern == stack_info[1]:
    #             pos_stacks.append(stack)
    #         elif config.neg_pattern == stack_info[1]:
    #             neg_stacks.append(stack)
    #         else:
    #             error += stack["name"] + ": group info not found." + "\n"
    #     if config.order == "ordered":
    #         pos_stacks.sort(key=lambda pos_stack: int(pos_stack["name"].split("_")[0]))
    #     else:
    #         random.shuffle(pos_stacks)
    #     imgsets = []
    #     for pos_stack in pos_stacks:
    #         imgset = []
    #         pos_stack_info = pos_stack["name"].split("_")
    #         group_info = pos_stack_info[2]
    #         neg_stacks_group = [neg_stack for neg_stack in neg_stacks if group_info == neg_stack["name"].split("_")[2]]
    #         if len(neg_stacks_group) < (imgset_size-1):
    #             error += "Not enough negative images found for " + pos_stack["name"] + "\n"
    #             continue
    #         # pick neg images
    #         for rand_int in random.sample(range(len(neg_stacks_group)), imgset_size-1):
    #             imgset.append(copy.copy(neg_stacks_group[rand_int]))
    #         # add pos stack
    #         imgset.insert(random.randint(0,imgset_size),pos_stack)
    #         for i in range(imgset_size):
    #             imgset[i]["div_id"] = config.div_ids[i]
    #         imgsets.append(imgset)
            
    #     return imgsets,error


    # def auto_create_ROClike_imgsets(self, image_stacks, config):
    #     imgset_size = len(config.div_ids)
    #     if config.order == "random":
    #         random.shuffle(image_stacks)
    #     else:
    #         image_stacks.sort(key=lambda stack: stack["name"].split("_")[0])
    #     imgsets = []
    #     error = None
    #     for i in range(0,len(image_stacks) - imgset_size + 1, imgset_size):
    #         imgset = image_stacks[i:i+imgset_size]
    #         for i, stack in enumerate(imgset):
    #             stack["div_id"] = config.div_ids[i]
    #         imgsets.append(imgset)

    #     if config.order == "random":
    #         random.shuffle(imgsets)

    #     return imgsets,error
        
# class Imgset_config:
#     def __init__(self,config_dict):
#         self.pos_pattern = config_dict["pos_pattern"] 
#         self.neg_pattern = config_dict["neg_pattern"]
#         self.stackmode = config_dict["stackmode"]  
#         self.ref_stack_name = config_dict["ref_stack_name"] 
#         self.div_ids = config_dict["div_ids"] 
#         self.div_ids_ref = config_dict["div_ids_ref"] 
#         self.viewport = config_dict["viewport"] 
#         self.viewport_ref = config_dict["viewport_ref"] 
#         self.imgset_type = config_dict["imgset_type"] 
#         self.order = config_dict["order"] 
#         self.stackmode = config_dict["stackmode"]



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
    img_height = db.Column(db.Integer())
    img_height_auto = db.Column(db.Boolean)
    img_per_row = db.Column(db.Integer())
    numb_rois = db.Column(db.Integer())
    show_viewport_info = db.Column(db.Boolean)
    transition_time = db.Column(db.Integer())
    randomize_order = db.Column(db.Boolean)
    scales = db.relationship("Scale", lazy=True, cascade="all, delete-orphan")
    tools = db.relationship("Tool", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
            design_dict = {}
            design_dict["id"] = self.id
            design_dict["study_id"] = self.study_id
            design_dict["instructions"] = self.instructions
            design_dict["button_labels"] = self.button_labels
            design_dict["background_color"] = self.background_color
            design_dict["text_color"] = self.text_color
            design_dict["numb_img"] = self.numb_img
            design_dict["numb_refimg"] = self.numb_refimg
            design_dict["img_per_row"] = self.img_per_row
            design_dict["img_height"] = self.img_height
            design_dict["img_height_auto"] = self.img_height_auto
            design_dict["numb_rois"] = self.numb_rois
            design_dict["show_viewport_info"] = self.show_viewport_info
            design_dict["transition_time"] = self.transition_time
            design_dict["randomize_order"] = self.randomize_order
            design_dict["scales"] = [scale.to_dict() for scale in self.scales]
            design_dict["tools"] = [tool.to_dict() for tool in self.tools]

            return design_dict


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
        self.numb_img=1
        self.numb_refimg=0
        self.img_height=512
        self.img_height_auto=True
        self.img_per_row = 1
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
    labels = db.Column(db.String(1000))
    text = db.Column(db.String(1000))
    labels = db.Column(db.String(1000))
    type = db.Column(db.String(20))

    def to_dict(self):
        scale_dict = {}
        scale_dict["id"] = self.id
        scale_dict["design_id"] = self.design_id
        scale_dict["min"] = self.min
        scale_dict["max"] = self.max
        scale_dict["text"] = self.text
        scale_dict["type"] = self.type
        # fix for compatibility with old db design
        if self.labels:
            scale_dict["labels"] = json.loads(self.labels)
        else:
            scale_dict["labels"] = [i for i in range(self.min, self.max + 1)]
        return scale_dict

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
    settings = db.Column(db.String(1000))

    def to_dict(self):
        tool_dict = {}
        tool_dict["cs_name"] = self.cs_name
        tool_dict["key_binding"] = self.key_binding
        try:
            tool_dict["settings"] = json.loads(self.settings)
        except:
            tool_dict["settings"] = self.settings
        
        return tool_dict


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
    scale_input = db.Column(db.String(10000))


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
    imgsets_finished = db.Column(db.Integer(),nullable=False)
    updated = db.Column(db.DateTime(), server_default=db.func.now(),
                        server_onupdate=db.func.now())

    def to_dict(self):
        dict = {}
        dict["user_id"] = self.user_id
        dict["username"] = self.user.username
        dict["imgsets_finished"] = self.imgsets_finished
        dict["updated"] = self.updated

        return dict   


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
    image_stacks = db.relationship("Image_stack",backref="imgset", lazy=False, cascade="all, delete-orphan")

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

    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["base_url"] = self.base_url
        dict["name"] = self.name
    
        return dict


#table for m to n relationships (image_stacks - images)
# stack_images = db.Table("stack_images",
#     db.Column("image_stack_id",db.Integer, db.ForeignKey("image_stack.id"), primary_key=True),
#     db.Column("image_id",db.Integer, db.ForeignKey("image.id"), primary_key=True)
# )
    


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
    # images = db.relationship("Image",secondary=stack_images, backref=db.backref("image_stacks", lazy=True),lazy='subquery', order_by='Image.name')
    viewport = db.Column(db.String(1000))
    tool_state = db.Column(db.Text(1000000))
    seg_data = db.Column(db.Text(100000000))

    def to_dict(self):
        image_stack_dict = {}
        image_stack_dict["div_id"] = self.div_id
        image_stack_dict["name"] = self.name
        image_stack_dict["cs_stack"] = {"imageIds":[],
                                        "currentImageIdIndex":0}
        images = self.get_images()
        for image in images:
            url = os.path.join(image.base_url,image.name)
            if ".dcm" in image.name.lower():
                url = "wadouri:" + url                
            image_stack_dict["cs_stack"]["imageIds"].append(url)
        image_stack_dict["cs_stack"]["imageIds"]
        image_stack_dict["cs_stack"]["imageIds"].sort()
        if self.viewport:
            image_stack_dict["viewport"] = json.loads(self.viewport)
        if self.tool_state:
            image_stack_dict["tool_state"] = json.loads(self.tool_state)
        
        image_stack_dict["seg_data"] = self.seg_data
        
        return image_stack_dict

    def get_images(self):
        if self.imgset:
            images = [image for image in self.imgset.study.images if image.base_url.split(os.sep)[-2] == self.name]
        else:
            images = [image for image in self.result.study.images if image.base_url.split(os.sep)[-2] == self.name]
        return images

    def save_seg_data(self,file_path):
        data = json.loads(self.seg_data)
        arrays1d = data[0:-1]
        x_res = data[-1][0]
        y_res = data[-1][1]
        arrays2d = []
        for array1d in arrays1d:
            if array1d:
                array1d_temp = np.array(array1d,dtype=np.int16)
            else:
                array1d_temp = np.zeros(x_res*y_res)
            array1d_temp = array1d_temp.reshape(x_res,y_res)
            array1d_temp = np.flip(array1d_temp,1)
            array1d_temp = np.rot90(array1d_temp)

            arrays2d.append(array1d_temp)
                        
        array3d = np.stack(arrays2d,-1)
        new_image = nib.Nifti1Image(array3d, affine=np.eye(4))
        new_image.header.get_xyzt_units()
        new_image.to_filename(file_path)       


#### none db model classes
# might be possible to move all of these classes and functions to the database model
# not done so far since the design and requirments 
# of scale input and tool data kept changing during development => compatibility to old dbs easier
# both of these dont have their own table rigth now
class Output:
    """
    Class to handle the conversion of data from the db tables to the outputfile
    

    Args:
       study_id

    Attributes:
       table_header
       col_info
       table_data 
    """

    def __init__(self,study):
        self.study = study
        # meta data
        self.row_numb = 0
        self.max_stack_size = 0
        self.incl_expl = False
        # cols always present
        self.imgset = {"imgset_id":[]} 
        self.user = {"username":[]}
        self.date = {"date":[]}
        self.stacks_disp = {}
        for i in range(self.study.design.numb_img):
            self.stacks_disp["stack-%s"%str(i+1)] = []
            self.stacks_disp["stack-%s-files"%str(i+1)] = []
        self.stack_user = {"stack-user":[], "stack-user-files":[]}
        # cols optional
        self.ref_stacks = {}
        for i in range(self.study.design.numb_refimg):
            self.ref_stacks["ref-stack-%s"%str(i+1)] = []
            self.ref_stacks["ref-stack-%s-files"%str(i+1)] = []
        self.scale_input = {}
        self.tool_gt = {}
        self.tool_input = {}
        self.overlap_data = {}
        

    def get_data(self,users):
        for result in self.study.results:
            # col always present
            self.get_imgset_data(result)
            self.get_user_data(result,users)
            self.get_img_disp_data(result)
            self.get_date_data(result)
            self.get_img_user_data(result)
            # optional columns
            self.get_ref_img_data(result)
            self.get_scale_data(result)
            self.get_tool_gt_data(result)
            self.get_tool_input_data(result)
            self.row_numb += 1

    # get data for columns always present
    def get_imgset_data(self,result):
        self.imgset["imgset_id"].append(result.imgset.position)


    def get_user_data(self,result,users):
        username = [user.username for user in users if user.id == result.user_id][0]
        self.user["username"].append(username)    


    def get_img_disp_data(self,result):
        for i in range(self.study.design.numb_refimg, self.study.design.numb_img + self.study.design.numb_refimg):
            div_id = "dicom_img_" + str(i)
            stack = result.imgset.get_stack_by_div_id(div_id)
            stack_col_index = str(i+1 - self.study.design.numb_refimg)
            stack_col_name = f"stack-{stack_col_index}"
            stack_files_col_name = f"stack-{stack_col_index}-files"
            # stack can be none if left blank
            if stack:
                image_names = [image.name for image in stack.get_images()]
                self.stacks_disp[stack_col_name].append(stack.name)
                self.stacks_disp[stack_files_col_name].append(image_names)
                self.max_stack_size = max(self.max_stack_size,len(image_names))
            else:
                self.stacks_disp[stack_col_name].append(None)
                self.stacks_disp[stack_files_col_name].append(None)

    def get_img_user_data(self,result):
        stack_picked = result.stack_picked
        # stack can be none if left blank
        if stack_picked:
            image_names = [image.name for image in stack_picked.get_images()]
            self.stack_user["stack-user"].append(stack_picked.name)
            self.stack_user["stack-user-files"].append(image_names)
        else:
            self.stack_user["stack-user"].append(None)
            self.stack_user["stack-user-files"].append(None)

   
    def get_date_data(self,result):
        self.date["date"].append(result.created)

    # get data for optional columns
    def get_ref_img_data(self,result):
        for i in range(self.study.design.numb_refimg):
            div_id_ref = "dicom_img_" + str(i)
            stack = result.imgset.get_stack_by_div_id(div_id_ref)
            # stack can be none if left blank
            if stack:
                image_names = [image.name for image in stack.get_images()]
                self.ref_stacks["ref-stack-%s"%str(i+1)].append(stack.name)
                self.ref_stacks["ref-stack-%s-files"%str(i+1)].append(image_names)
                self.max_stack_size = max(self.max_stack_size,len(image_names))
            else:
                self.ref_stacks["ref-stack-%s"%str(i+1)].append(None)
                self.ref_stacks["ref-stack-%s-files"%str(i+1)].append(None)

    def get_scale_data(self,result):
        if result.scale_input:
            scale_input = json.loads(result.scale_input)
            # scale input is a list of dictonaries with sub-dictonaries
            # dict keys are the scale text
            # sub-dict keys are values (scale input collected from user) and uuid (was used to link scale data to annotations i.e. rois)
            # values and uuids are lists as scales can be repeated (FROC studies)
            for scale_text in scale_input.keys():
                values = scale_input[scale_text]["values"]
                scale_header = scale_text
                if scale_header in self.scale_input.keys():
                    self.scale_input[scale_header].append(values)
                else:
                    self.scale_input[scale_header] = [None] * self.row_numb + [values]
            # ensure all cols have same length
            for k,v in self.scale_input.items():
                if k not in scale_input.keys():
                    v.append(None)
        else:
            # ensure all cols have same length
            for k,v in self.scale_input.items():
                v.append(None)

    def get_tool_gt_data(self,result):
        for i in range(self.study.design.numb_img):
            div_id_ref = "dicom_img_%s"%str(i+2)
            stack = result.imgset.get_stack_by_div_id(div_id_ref)
            # stack can be none if left blank
            if stack and stack.tool_state:
                stack_tool_states = json.loads(stack.tool_state)
                # stack tools state is list of cornerstone tool states
                # each entry corresponds to an image within the stack
                # each image tool state can consist of multiple tool input
                for img in range(len(stack.get_images())):
                    tool_state = stack_tool_states[img]
                    if tool_state:
                        for tool in tool_state:
                            col_name = "stack-%s-pos-%s-%s"%(i+1,img+1,tool)
                            if col_name in self.tool_gt.keys():
                                self.tool_gt[col_name].append(tool_state[tool]["data"])
                            else:
                                self.tool_gt[col_name] = [None] * self.row_numb + [tool_state[tool]["data"]]
        # ensure all cols have same length
        for k, v in self.tool_gt.items():
            if len(v) < self.row_numb+1:
                v.append(None)


    def get_tool_input_data(self,result):
        if result.stack_picked.tool_state:
            stack_tool_states = json.loads(result.stack_picked.tool_state)
            # stack tools state is list of cornerstone tool states
            # each entry corresponds to an image within the stack
            # each image tool state can consist of multiple tool inputs
            for i in range(len(result.stack_picked.get_images())):
                tool_state = stack_tool_states[i]
                if tool_state:
                    for tool in tool_state:
                        col_name = "stack-user-pos-%s-%s"%(i+1,tool)
                        # col already exists
                        if col_name in self.tool_input.keys():
                            self.tool_input[col_name].append(tool_state[tool]["data"])
                        # col is new
                        else:
                            self.tool_input[col_name] = [None] * self.row_numb + [tool_state[tool]["data"]]
        # ensure all cols have same length
        for k,v in self.tool_input.items():
            if len(v) < self.row_numb+1:
                v.append(None)


    def calc_overlap_data(self):
        rois_cols_input = {k: v for k, v in self.tool_input.items() if "Roi" in k}

        if not rois_cols_input:
            return

        for row in range(self.row_numb):
            stack_name_user = self.stack_user["stack-user"][row]
            gt_ind= int([k.split("-")[1] for k,v in self.stacks_disp.items() if v[row] == stack_name_user][0]) 
            for k_input, v_input in rois_cols_input.items():
                roi_type = k_input.split("-")[4]
                stack_pos_input = k_input.split("-")[3]
                col_name_gt = "stack-%s-pos-%s-%s"%(str(gt_ind),stack_pos_input,roi_type)
                
                rois_input = v_input[row]
                rois_gt = None
                if col_name_gt in self.tool_gt:
                    rois_gt = self.tool_gt[col_name_gt][row]                   
                if not rois_gt or not rois_input or len(rois_gt) == 0 or len(rois_input) == 0:
                    continue
                # iterate over rois and calc metrics
                for metric in ["dice"]:
                    ov_gt = np.zeros(shape=(len(rois_gt),len(rois_input)))
                    ov_input = np.zeros(shape=(len(rois_input),len(rois_gt)))
                    for i, roi_gt in enumerate(rois_gt):
                        roi_gt = getRoiObject(roi_type, roi_gt) 
                        for j, roi_input in enumerate(rois_input):
                            roi_input = getRoiObject(roi_type, roi_input)
                            overlap = roi_gt.calc_seq_metric(roi_input, metric)
                            ov_gt[i][j] = overlap
                            ov_input[j][i] = overlap
                            
                    col_name_gt = col_name_gt + "-%s"%(metric)
                    ov_gt = [max(ov) for ov in ov_gt]
                    if col_name_gt in self.overlap_data.keys():
                        self.overlap_data[col_name_gt].append(ov_gt)                            
                    else:
                        self.overlap_data[col_name_gt] = [None] * row + [ov_gt]

                    col_name_input = k_input + "-%s"%(metric)
                    ov_input = [max(ov) for ov in ov_input]
                    if col_name_input in self.overlap_data.keys():
                        self.overlap_data[col_name_input].append(ov_input)                            
                    else:
                        self.overlap_data[col_name_input] = [None] * row + [ov_input]  
              
            # ensure all cols have same length
            for k, v in self.overlap_data.items():
                if len(v) < row+1:
                    v.append(None)



    def save_table(self,format = "excel", include_ov=True, include_raw_tool_data=False, include_expl=False):
        # combine data into pandas dataframe
        self.df = pd.DataFrame({**self.imgset,**self.user,**self.stacks_disp,**self.date,**self.scale_input,**self.stack_user})
        for k,v in self.ref_stacks.items():
            self.df[k] = v
        for k,v in self.tool_gt.items():
            self.df[k] = v
        for k,v in self.tool_input.items():
            self.df[k] = v


        # add formatting e.g. col names, col splitting ....
        self.format_tool_data(include_raw_tool_data)

        if include_ov:
            # calc metrics (e.g. dice, iou)
            self.calc_overlap_data()
            for k,v in self.overlap_data.items():
                self.df[k] = v

        # to do, add sepecial case for max stack size = 1
        self.format_simplify()        

        if format == "excel":
            filepath=os.path.join(current_app.config["IMAGE_PATH"],"results_study_%s.xlsx" % self.study.id)
            self.df.to_excel(filepath, index=False)
        else:
            filepath=os.path.join(current_app.config["IMAGE_PATH"],"results_study_%s.xlsx" % self.study.id)
            self.df.to_csv(filepath, index=False)


    def format_tool_data(self,include_raw_tool_data):
        self.format_roi_data(include_raw_tool_data)
        self.format_length_data(include_raw_tool_data)
        self.format_segmentation_data(include_raw_tool_data)


    def format_roi_data(self,include_raw_tool_data):
        rois_cols = [column for column in self.df if "Roi" in column and not "dice" in column]
        for roi_col in rois_cols:
            roi_type = roi_col.split("-")[4]
            area_col, mean_HU_col, sd_HU_col, start_col, end_col = [], [], [], [], []
            for imgset in range(self.row_numb):
                rois = self.df[roi_col][imgset]
                area_img, mean_HU_img, sd_HU_img, start_img, end_img = [], [], [],[], []
                if rois:
                    for roi in rois:
                        roi = getRoiObject(roi_type, roi)
                        area, mean_HU, sd_HU = roi.get_stats()                            
                        start, end = roi.get_coords()   
                        area_img.append(area), mean_HU_img.append(mean_HU), sd_HU_img.append(sd_HU)
                        start_img.append(start), end_img.append(end)
                area_col.append(area_img), mean_HU_col.append(mean_HU_img), sd_HU_col.append(sd_HU_img)
                start_col.append(start_img), end_col.append(end_img)            
            # add roi stats and coords
            self.df[roi_col + "-area"] = area_col
            self.df[roi_col + "-mean_HU"] = mean_HU_col
            self.df[roi_col + "-sd_HU"] = sd_HU_col
            self.df[roi_col + "-start"] = start_col
            self.df[roi_col + "-end"] = end_col

            if not include_raw_tool_data:
                self.df.drop(roi_col,inplace=True,axis=1)



    def format_length_data(self,include_raw_tool_data):
        length_cols = [column for column in self.df if "Length" in column]
        for length_col in length_cols:
            start_col, end_col, len_col = [], [], []
            for imgset in range(self.row_numb):
                lengths = self.df[length_col][imgset]
                start_img, end_img, length_img, = [], [], []
                if lengths:
                    for length in lengths:
                        length = Length(length)
                        l = length.get_stats()                            
                        start, end = length.get_coords()   
                        start_img.append(start), end_img.append(end), length_img.append(l)
                start_col.append(start_img), end_col.append(end_img), len_col.append(length_img)            
            # add roi stats and coords
            self.df[length_col + "-start"] = start_col
            self.df[length_col + "-end"] = end_col
            self.df[length_col + "-length"] = len_col

            if not include_raw_tool_data:
                self.df.drop(length_col,inplace=True,axis=1)

    def format_segmentation_data(self,include_raw_tool_data):
        pass

    def format_simplify(self):
        # if stack size = 1 (single images evaluated)
        # output can be simplified (remove file cols and list structure tool cols)
        if self.study.design.numb_img == 1:
            for col in self.stack_user.keys():
                self.df.drop(col,inplace=True,axis=1)
        
        if self.max_stack_size == 1:
            columns_names = {}
            for col in self.df:
                if "files" in col:
                    self.df.drop(col,inplace=True,axis=1)
                if "stack" in col:
                    col_split = col.split("-")
                    stack_ind = col_split[1]
                    if len(col_split) > 2:
                        columns_names[col] = col.replace("stack-%s-pos-1"%stack_ind,"image-%s"%stack_ind)
                    else:
                        columns_names[col] = col.replace("stack-%s"%stack_ind,"image-%s"%stack_ind)


            self.df.rename(columns=columns_names, inplace=True)

        # rm emtpy lists and None from results    
        self.df = self.df.applymap(lambda x: None if x == [] else x )
        self.df = self.df.applymap(lambda x: x[0] if type(x) is list and len(x) == 1 else x )

        # sort cols 
        # self.df = self.df.reindex(sorted(self.df.columns), axis=1)


def getRoiObject(roi_type, roi_data):
    """
    Args:
       roi_type roi_data

    """
    if "EllipticalRoi" in roi_type:
        roi = EllipticalRoi(roi_data)
    elif "CircleRoi" in  roi_type:
        roi = CircleRoi(roi_data)
    elif "RectangleRoi" in  roi_type:
        roi = RectangleRoi(roi_data)
    elif "FreehandRoi" in  roi_type:
        roi = FreehandRoi(roi_data)

    return roi

class Annotation:
    """
    Class to handle annotation data (rois, length measuerments) collected with cornerstone tools (javascript library)

    Args:
       tool_state_raw (dict in json format)

    Attributes:
       tool_state_raw (dict): stores the raw toolstate data
    """
    def __init__(self,tool_state_raw):
        self.uuid = tool_state_raw["uuid"]
        self.start_x = tool_state_raw["handles"]["start"]["x"]
        self.start_y = tool_state_raw["handles"]["start"]["y"]
        self.end_x = tool_state_raw["handles"]["end"]["x"]
        self.end_y = tool_state_raw["handles"]["end"]["y"]


    def get_tool_state_string(self):
        return(json.dumps(self.annotations))

    def get_coords(self):
        return (round(self.start_x,2),round(self.start_y,2)),\
               (round(self.end_x,2),round(self.end_y,2))

class Length(Annotation):
    def __init__(self, tool_state_raw):
        super().__init__(tool_state_raw)
        self.length = tool_state_raw["length"]

    def set_polygon(self):
        """
            generate shapley linestrings from annotation data and store them
        """
        line = LineString([(self.start_x,self.start_y),(self.end_x,self.end_y)])
        self.line = line

    def get_stats(self):
        return round(self.length,2)

class Rois(Annotation):
    def __init__(self, tool_state_raw):
        super().__init__(tool_state_raw)
        self.area = tool_state_raw["cachedStats"]["area"]
        self.mean = tool_state_raw["cachedStats"]["mean"]
        self.sd = tool_state_raw["cachedStats"]["stdDev"]

    def calc_seq_metric(self,roi,metric):
        self.set_polygon()
        roi.set_polygon()
        result = eval(metric + "(self.polygon , roi.polygon)")
        result = round(result,2)
        return(result)

    def get_stats(self):
        return round(self.area,2), round(self.mean,2), round(self.sd,2)


class EllipticalRoi(Rois):
    def set_polygon(self):
        """
            generate shapley polygons from annotation data and store them
        """
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        center_x = (self.end_x  + self.start_x)/2
        center_y = (self.end_y + self.start_y)/2
        angle = 0 
        
        #Generate an ellipse using shapely. For more information see:
        #https://gis.stackexchange.com/questions/243459/drawing-ellipse-with-shapely
        center = Point((center_x,center_y))
        circle = center.buffer(1)
        ellipsis = scale(circle,(width/2),(height/2))
        ellipsis = rotate(ellipsis,angle)
        
        self.polygon = ellipsis
        
class CircleRoi(Rois):
    def set_polygon(self):
        """
            generate shapley polygons from annotation data and store them
        """
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        center_x = (self.end_x  + self.start_x)/2
        center_y = (self.end_y + self.start_y)/2
        
        #Generate an ellipse using shapely. For more information see:
        #https://gis.stackexchange.com/questions/243459/drawing-ellipse-with-shapely
        center = Point((center_x,center_y))
        circle = center.buffer(1)
        circle = scale(circle,(width/2),(height/2))
        
        self.polygon = circle


class RectangleRoi(Rois):
     def set_polygon(self):
        """
            generate shapley polygons from annotation data and store them
        """     
        center_x = (self.end_x + self.start_x)/2
        center_y = (self.end_y + self.start_x)/2
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        rectangle = Polygon([(center_x - width/2, center_y + height/2),
                             (center_x + width/2, center_y + height/2),
                             (center_x + width/2, center_y - height/2),
                             (center_x - width/2, center_y - height/2)])
        self.polygon = rectangle


class FreehandRoi(Rois):
    def __init__(self, tool_state_raw):
        self.uuid = tool_state_raw["uuid"]
        self.points = []
        for point in tool_state_raw["handles"]["points"]:
            self.points.append(Point(point["x"],point["y"]))

    def set_polygons(self):
        """
        generate shapley polygons from annotation data and store them
        """
        polygon = Polygon(self.points)
        self.polygon = polygon

    def get_coords(self):
        return round(self.points[0],2), round(self.points[-1],2)


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
        return iou

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
        dice = (2*area_intersection)/(polygon_1.area + polygon_2.area) * 100
        return dice

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
            return perc_intersect 
        except:
            return -1


# comand line functions
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
    try:
        os.mkdir(image_folder)
        click.echo("Initialized dir for images.")
    except:
        click.echo("Could not initialize dir for images.")

#needed for tests etc
def add_default_users():
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

@click.command("init-imgdir")
@with_appcontext
def init_imgdir_command():
    init_img_dir()

@click.command("add-default-users")
@with_appcontext
def add_default_users_command():
    add_default_users()

@click.command("init-app")
@with_appcontext
def init_all_command():
    init_db()
    init_img_dir()
    add_default_users()


# def database changes for vue update
def updateDB():
    return
