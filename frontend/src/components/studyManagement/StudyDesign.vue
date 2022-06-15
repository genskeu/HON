<template>
  <div class="container-fluid h-100 mt-4" id="content">
    <div class="row mx-auto my-auto h-100">
      <!-- Sidebar for ImgSets (left)
                                <div class="col-lg-2">
                                    <div class="row mx-auto sticky-top" style="top:4em;">
                                        <button class="btn btn-dark col-12 mb-2 sticky-top" data-bs-toggle="collapse"
                                            data-bs-target="#sidebar" aria-expanded="true" aria-controls="sidebar" data-placement="left"
                                            title="Image-Sets that will be shown to users during the study.
                    The currently selected image-set will be highlited green.">
                                            <h4 class="w-100 mt-1" id="imgset_btn">Image-Sets &#9776;</h4>
                                        </button>
                                    </div>
                                    <div class="sidebar_own sticky-top bg-secondary collapse show" id="sidebar">
                                        <div class="row">
                                            <button class='imgset btn btn-light col-lg-12' id="imgset_"
                                                action="">
                                                Image Set
                                            </button>
                                        </div>
                                    </div>
                                </div> -->
      <!-- Imgsets -->
      <div class="col-lg-10 h-100 mb-2">
        <div class="row w-100 mx-auto">
          <button
            class="btn btn-dark mb-2"
            data-bs-toggle="collapse"
            data-bs-target="#imgset_creation"
            aria-expanded="true"
            aria-controls="imgset_creation"
          >
            <h4 class="mt-1">Image Sets &#9776;</h4>
          </button>
        </div>
        <!-- Create Image Sets -->
        <div id="imgset_creation" class="collapse show row mx-auto my-auto h-100">
          <!-- Display warning if the study already started (results are present)
                                 User can still modify design but should be aware that this can cause bugs
                                -->
          <div id="imgset" class="w-100 h-100">
            <!--Images -->

            <div id="ref_images">
              <span class="badge badge-secondary w-100 mb-2">
                <h4 class="mt-1">Reference Image Stack(s)</h4>
              </span>
            </div>
            <div id="comp_images" class="h-100">
              <span class="badge badge-secondary w-100 mb-2">
                <h4 class="mt-1">Image Stack(s)</h4>
              </span>
                <div class="relative h-full grid p-4 gap-2 grid-cols-3">
                    <dicom-viewer></dicom-viewer>
                    <dicom-viewer></dicom-viewer>
                </div>
              <div
                class="row justify-content-center mx-auto"
                id="dicom_row_"
              ></div>
            </div>
            <!-- modify buttons -->
            <div id="imgset_buttons">
              <div class="row mt-3 mb-2">
                <div class="col-lg-12 text-center">
                  <input
                    type="button"
                    value="append imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="add_imgset"
                    title="add image-set to the end of the study"
                  />
                  <input
                    type="button"
                    value="insert imgset"
                    class="imgset_btn btn-success btn col-lg-2"
                    id="insert_imgset"
                    title="inserts image-set at the currently selected position"
                  />
                  <input
                    type="button"
                    value="update imgset"
                    class="imgset_btn btn-light btn col-lg-2"
                    id="upd_imgset"
                    title="update currently selected image-set"
                  />
                  <input
                    type="button"
                    value="delete imgset"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_imgset"
                    title="delete currently selected image-set"
                  />
                  <input
                    type="button"
                    value="delete all imgsets"
                    class="imgset_btn btn-danger btn col-lg-2"
                    id="del_all_imgsets"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- sidebar for design, viewport settings, scales etc (rigth) -->
      <div class="col-lg-2">
        <!-- Design Settings -->
        <div class="row mx-auto">
          <button
            class="btn btn-dark col-12 mb-1"
            data-bs-toggle="collapse"
            data-bs-target="#design_settings"
            title="Click on the sections to expand the sub-menus.
                    Study design options were divided into general settings, tools, instructions and scales.
                    After changing any design options dont forget to press the Save Design button.
                              "
            aria-expanded="true"
            aria-controls="design_settings"
          >
            <h4 class="w-100 mt-1">Design Options &#9776;</h4>
          </button>
        </div>
        <div id="design_settings" class="collapse show">
          <!-- General Settings -->
          <div class="row mx-auto mt-1">
            <button
              class="btn-secondary btn col-12"
              data-bs-toggle="collapse"
              data-bs-target="#general_settings"
              aria-expanded="true"
              aria-controls="general_settings"
              title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously."
            >
              <h5 class="mt-1">General Settings</h5>
            </button>
          </div>
          <div id="general_settings" class="collapse">
            <div class="mx-auto">
              <div
                class="input-group row mx-auto"
                title="Controls max number of reference images"
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Ref-Images</span>
                </div>
                <select class="custom-select" id="numb_refimg">
                  <option value=""></option>
                </select>
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls the number of images (m-AFC tests)"
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Images</span>
                </div>
                <select class="custom-select" id="numb_img">
                  <option value=""></option>
                </select>
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls the number of annotations (e.g. rois)
                    that need to be drawn by participants
                    before evaluating the next picture.
                    Set to 0 to allow any number."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12"># Annotations</span>
                </div>
                <input
                  class="form-control"
                  type="Number"
                  step="any"
                  id="numb_rois"
                  min="0"
                />
              </div>

              <!-- window size -->
              <div class="row mx-auto">
                <div
                  class="input-group"
                  title="Controls the size (width, height) of the screen section used for displaying images."
                >
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Viewport-Size</span>
                  </div>
                  <input
                    id="img_width"
                    type="Number"
                    step="any"
                    class="image_size form-control"
                    placeholder="width"
                  />
                  <input
                    id="img_height"
                    type="Number"
                    step="any"
                    class="image_size form-control"
                    placeholder="height"
                  />
                </div>
              </div>

              <div class="input-group row mx-auto">
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Text Color</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  id="text_color"
                  placeholder="Text-Color (Hex or Name)"
                  value=""
                />
              </div>

              <div class="input-group row mx-auto">
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">BG Color</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  id="background_color"
                  placeholder="Background-Color (Hex or Name)"
                  value=""
                />
              </div>

              <div
                class="input-group row mx-auto"
                title="Time (sec) the screen will be blank between two image-sets."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Transition Time</span>
                </div>
                <input
                  class="form-control"
                  type="number"
                  min="0"
                  name="instructions"
                  id="transition_time"
                  placeholder="sec"
                  value=""
                />
              </div>

              <div
                class="row input-group mx-auto"
                title="Controls the text of the buttons displayed beneath each image to continue to the next image-set."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Button Label</span>
                </div>
                <input
                  class="form-control"
                  type="text"
                  name="buttonLabels"
                  id="button_labels"
                  placeholder="Btn Label"
                />
              </div>

              <div
                class="input-group row mx-auto"
                title="Controls if image settings such as windowing or zoom level are displayed."
              >
                <div class="input-group-prepend col-6 px-0 mx-0">
                  <span class="input-group-text col-12">Img Viewer Info</span>
                </div>
                <input
                  type="button"
                  name="show_display"
                  id="show_viewport_info"
                />
              </div>
            </div>
          </div>
          <!-- tool settings -->
          <div class="row mx-auto mt-1">
            <button
              class="btn-secondary btn col-12"
              data-bs-toggle="collapse"
              data-bs-target="#tools"
              aria-expanded="true"
              aria-controls="tools"
              title="Tools define DICOM viewer and annotation tools that are made available to participants
                    (e.g., scrolling, windowing, rectangular, elliptical or free-hand ROIs)."
            >
              <h5 class="mt-1 col-12">Tools</h5>
            </button>
          </div>
          <div id="tools" class="collapse">
            <div class="row input-group text-center mx-auto">
              <div class="input-group-prepend text-dark w-100">
                <div class="input-group-text w-100">
                  <input
                    type="checkbox"
                    class="mr-3"
                    id=""
                    name="toolsCheck"
                    value=""
                  />
                </div>
              </div>
            </div>
          </div>
          <div
            class="row mx-auto mt-1"
            title="Instructions can be customized and are displayed to participants throughout studies."
          >
            <!-- instructions -->
            <button
              class="btn-secondary btn col-12"
              data-bs-toggle="collapse"
              data-bs-target="#instructions_container"
              aria-expanded="true"
              aria-controls="instructions_container"
            >
              <h5 class="mt-1 col-12">Instructions</h5>
            </button>
            <div id="instructions_container" class="w-100 collapse">
              <div class="input-group" id="instructions_input_field">
                <textarea
                  rows="3"
                  class="form-control"
                  type="text"
                  name="instructions"
                  id="instructions"
                  placeholder="Instructions"
                ></textarea>
              </div>
              <div
                id="instructions_user_view"
                style="white-space: pre-wrap"
              ></div>
            </div>
          </div>
          <!-- scales -->
          <div
            class="row mx-auto mt-1"
            title="Scales can be customized and are displayed to participants throughout studies."
          >
            <button
              class="btn btn-secondary col-12"
              data-bs-toggle="collapse"
              data-bs-target="#scales_container"
              aria-expanded="true"
              aria-controls="scales_container"
            >
              <h5 class="mt-1">Scale(s)</h5>
            </button>
          </div>
          <div id="scales_container" class="collapse">
            <div class="row mx-auto">
              <button class="btn btn-success btn-block col" id="add_scale">
                add scale
              </button>
            </div>

            <div id="scales" class="mt-1">
              <!-- templetate to create new scales using js -->
              <div
                id="scale_"
                class="mt-1 scale_template"
                style="display: none"
              >
                <span class="badge badge-light w-100 mt-1">
                  <h6 id="scale_heading_" class="mt-1 scale_heading">Scale</h6>
                </span>
                <!-- admin view to define scale -->
                <div class="mx-auto scale_view_admin" id="scale_view_admin_">
                  <div
                    class="row mx-auto scale_text_admin"
                    id="scale_text_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Text</span>
                      </div>
                      <textarea
                        id="scale_text_input_"
                        class="form-control scale_text_input"
                      ></textarea>
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_min_admin"
                    id="scale_min_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Start</span>
                      </div>
                      <input
                        class="form-control scale_min_input"
                        min="-100"
                        max="100"
                        type="number"
                        id="scale_min_input_"
                        placeholder="min"
                        value=""
                      />
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_max_admin"
                    id="scale_max_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">End</span>
                      </div>
                      <input
                        class="form-control scale_max_input"
                        min="-100"
                        max="100"
                        type="number"
                        id="scale_max_input_"
                        placeholder="max"
                        value=""
                      />
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_type_admin"
                    id="scale_type_admin_"
                    title="Can be left blank for most studies except for FROC designs,
                    where a scale needs to be repeated each time a new roi is drawn."
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Type</span>
                      </div>

                      <select
                        id="scale_type_input_"
                        class="custom-select scale_type_input"
                      >
                        <option value=""></option>
                        <option value=""></option>
                      </select>
                    </div>
                  </div>
                  <button
                    class="btn btn-danger btn-block scale_rm"
                    id="scale_rm_"
                  >
                    rm scale
                  </button>
                </div>
                <!-- participant view of scale -->
                <div class="mx-auto mb-3 scale_view_user" id="scale_view_user_">
                  <div class="row mx-auto justify-content-center">
                    <div
                      id="scale_text_"
                      class="col scale_text"
                      style="white-space: pre-wrap; text-align: center"
                    ></div>
                  </div>
                  <div
                    class="row mx-auto justify-content-center mt-1 scale_values"
                    id="scale_values_"
                    style="display: none"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          <!-- Save Design Settings -->
          <form method="post">
            <div class="form-group">
              <input
                class="btn btn-light btn-lg btn-block mt-1 w-100"
                type="button"
                id="submit_design"
                value="Save Design"
              />
            </div>
          </form>
        </div>

        <!-- default viewport settings -->
        <div
          id="viewport_settings_container"
          class="w-100"
          title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                    Each viewport can be controlled individually.
                    To globally control viewport settings use the defaults submenu."
        >
          <div class="row mt-1 mx-auto">
            <button
              class="btn btn-dark col-12 mb-2"
              data-bs-toggle="collapse"
              data-bs-target="#viewport_settings"
              aria-expanded="true"
              aria-controls="viewport_settings"
            >
              <h4 class="w-100 mt-1" id="imgset_btn">Image Viewer &#9776;</h4>
            </button>
          </div>
        </div>
        <div id="viewport_settings" class="mb-3 collapse show">
          <button
            class="btn btn-secondary btn-block"
            data-bs-toggle="collapse"
            data-bs-target="#viewport_def"
            aria-expanded="true"
            aria-controls="viewport_def"
          >
            <h5 class="mt-1 col-12">Defaults</h5>
          </button>
          <div id="viewport_def" class="collapse">
            <!-- ww/wc -->
            <div class="row mx-auto">
              <div class="input-group">
                <div class="input-group-prepend col-4 px-0 mx-0">
                  <span class="input-group-text col-12">WW/WC</span>
                </div>
                <input
                  id="def_ww"
                  type="Number"
                  step="any"
                  min="0"
                  class="form-control def_ww viewport_prop_def"
                  placeholder="WW"
                />
                <input
                  id="def_wc"
                  type="Number"
                  step="any"
                  min="0"
                  class="form-control def_wc viewport_prop_def"
                  placeholder="WC"
                />
              </div>
            </div>
            <!-- zoom -->
            <div class="row mx-auto">
              <div class="input-group">
                <div class="input-group-prepend col-4 px-0 mx-0">
                  <span class="input-group-text col-12">Zoom</span>
                </div>
                <input
                  id="def_zoom"
                  type="Number"
                  step="any"
                  min="0.0"
                  class="form-control def_zoom viewport_prop_def"
                  placeholder="Zoom"
                />
              </div>
            </div>
            <!-- position -->
            <div class="row mx-auto">
              <div class="input-group">
                <div class="input-group-prepend col-4 px-0 mx-0">
                  <span class="input-group-text col-12">Pos</span>
                </div>
                <input
                  id="def_pos_x"
                  type="Number"
                  step="any"
                  class="form-control def_pos_x viewport_prop_def"
                  placeholder="x"
                />
                <input
                  id="def_pos_y"
                  type="Number"
                  step="any"
                  class="form-control def_pos_y viewport_prop_def"
                  placeholder="y"
                />
              </div>
            </div>
            <div class="row mx-auto">
              <!-- position -->
              <button id="update_viewports" class="btn btn-light col-12">
                update existing image-sets
              </button>
            </div>
          </div>

          <div class="mx-auto" id="viewports">
            <!-- viewport info -->
            <div id="viewports_man_container">
              <div id="viewports_auto_container">
                <div id="viewport_info_">
                  <div class="row mx-auto mt-1">
                    <button
                      class="btn btn-secondary col-12"
                      data-bs-toggle="collapse"
                      data-bs-target="#viewport_"
                      aria-expanded="true"
                      aria-controls="viewport_"
                    >
                      <h5 class="mt-1">Viewer</h5>
                    </button>
                  </div>

                  <div id="viewport_" class="collapse">
                    <!-- windowing -->
                    <div class="row mx-auto">
                      <div class="input-group">
                        <div class="input-group-prepend col-4 px-0 mx-0">
                          <span class="input-group-text col-12">WW/WC</span>
                        </div>
                        <input
                          id="ww_"
                          type="Number"
                          step="any"
                          min="0"
                          class="form-control ww viewport_prop"
                          placeholder="WW"
                        />
                        <input
                          id="wc_"
                          type="Number"
                          step="any"
                          class="form-control wc viewport_prop"
                          placeholder="WC"
                        />
                      </div>
                    </div>
                    <!-- window zoom -->
                    <div class="row mx-auto">
                      <div class="input-group">
                        <div class="input-group-prepend col-4 px-0 mx-0">
                          <span class="input-group-text col-12">Zoom</span>
                        </div>
                        <input
                          id="zoom_"
                          type="Number"
                          step="any"
                          min="0.0"
                          class="form-control zoom viewport_prop"
                          placeholder="Zoom"
                        />
                      </div>
                    </div>
                    <!-- window position -->
                    <div class="row mx-auto">
                      <div class="input-group">
                        <div class="input-group-prepend col-4 px-0 mx-0">
                          <span class="input-group-text col-12">Pos</span>
                        </div>
                        <input
                          id="pos_x_"
                          type="Number"
                          step="any"
                          class="form-control pos_x viewport_prop"
                          placeholder="x"
                        />
                        <input
                          id="pos_y_"
                          type="Number"
                          step="any"
                          class="form-control pos_y viewport_prop"
                          placeholder="y"
                        />
                      </div>
                    </div>
                    <!--reset buttons -->
                    <button id="reset_" class="btn btn-block btn-light reset">
                      reset
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!--ROIs-->
        <div
          id="roi_settings_container"
          class="w-100 mb-1"
          style="display: none"
          title="The ROIs section shows the annotation coordinates drawn on each image.
                    ROIs can be drawn on images to define the ground truth in LROC and FROC studies."
        >
          <div class="row mx-auto roi_input">
            <button
              class="btn btn-dark col-12 mb-1"
              data-bs-toggle="collapse"
              data-bs-target="#roi_settings"
              aria-expanded="true"
              aria-controls="roi_settings"
            >
              <h4 class="w-100 mt-1">ROIs &#9776;</h4>
            </button>
          </div>
          <div id="roi_settings" class="collapse mb-3 show roi_input">
            <!-- roi info -->
            <div id="roi_info_img_" class="mt-1 ref_rois">
              <span class="badge-secondary badge col-12">
                <button
                  class="btn btn-secondary btn-block"
                  data-bs-toggle="collapse"
                  data-bs-target="#rois_img_"
                  aria-expanded="true"
                  aria-controls="rois_img_"
                >
                  <h5 class="col-12 mt-1">ROIs</h5>
                </button>
                <div id="rois_img_" class="collapse">
                  <div class="row text-center mx-auto">
                    <button
                      id="import_ann_"
                      class="btn btn-block btn-success import_ann col"
                    >
                      Import Rois From
                    </button>
                  </div>
                  <div class="row text-center mx-auto">
                    <div class="input-group">
                      <div class="input-group-prepend col-6 px-0 mx-0">
                        <span class="input-group-text col-12">Image-Set</span>
                      </div>
                      <input
                        id="import_ann_is_"
                        type="Number"
                        min="1"
                        class="form-control col"
                        placeholder=""
                      />
                    </div>
                  </div>
                  <div class="row text-center mx-auto">
                    <div class="input-group">
                      <div class="input-group-prepend col-6 px-0 mx-0">
                        <span class="input-group-text col-12"
                          >Image-Position</span
                        >
                      </div>
                      <input
                        id="import_ann_ip_"
                        type="Number"
                        min="1"
                        class="form-control col"
                        placeholder=""
                      />
                    </div>
                  </div>
                  <div class="row text-center mx-auto">
                    <div class="input-group">
                      <div class="input-group-prepend col-6 px-0 mx-0">
                        <span class="input-group-text col-12"
                          >Stack-Position</span
                        >
                      </div>
                      <input
                        id="import_ann_sp_"
                        type="Number"
                        min="1"
                        class="form-control col"
                        placeholder=""
                      />
                    </div>
                  </div>
                  <div class="row text-center mx-auto">
                    <!-- <button id=overlap class="btn btn-primary overlap">overlap</button> -->
                  </div>
                </div>
              </span>
            </div>
          </div>
        </div>

        <!--Segmentations-->
        <div
          id="seg_settings_container"
          class="w-100 mb-1"
          style="display: none"
          title=""
        >
          <div class="row mx-auto roi_input">
            <button
              class="btn btn-dark col-12 mb-1"
              data-bs-toggle="collapse"
              data-bs-target="#seg_settings"
              aria-expanded="true"
              aria-controls="seg_settings"
            >
              <h4 class="w-100 mt-1">Segmentation &#9776;</h4>
            </button>
          </div>
          <div id="seg_settings" class="collapse mb-3 show">
            <!-- roi info -->
            <div class="mt-1">
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Brush-Size</span>
                  </div>
                  <input
                    type="Number"
                    min="1"
                    class="form-control col"
                    value="10"
                    id="brush_size"
                  />
                </div>
              </div>
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Label</span>
                  </div>
                  <input
                    type="Number"
                    min="1"
                    class="form-control col"
                    value="1"
                    id="seg_label"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          id="results_container"
          class="w-100 mb-1"
          style="display: none"
          title="Load results from a study where annotation data was collected e.g. ROIs."
        >
          <div class="row mx-auto roi_input">
            <button
              class="btn btn-dark col-12 mb-1"
              data-bs-toggle="collapse"
              data-bs-target="#results"
              aria-expanded="true"
              aria-controls="results"
            >
              <h4 class="w-100 mt-1">Results &#9776;</h4>
            </button>
          </div>
          <div id="results" class="badge-light collapse show"></div>
        </div>

        <div class="row mt-2 mx-auto" style="display: none">
          <button class="btn btn-danger col-12 mb-2">
            <h4 class="w-100 mt-1" id="participant_view">Participant View</h4>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewer from '@/components/dicomViewer/DicomViewer.vue'

export default {
  name: 'Design',
  components: {
    DicomViewer
  }
}
</script>

<style>
</style>
