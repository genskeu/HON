<template>
  <div>
    <!--ROIs-->
    <div id="roi_settings_container" class="w-100 mb-1" style="display: none" title="The ROIs section shows the annotation coordinates drawn on each image.
                    ROIs can be drawn on images to define the ground truth in LROC and FROC studies.">
      <div class="row mx-auto roi_input">
        <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#roi_settings"
          aria-expanded="true" aria-controls="roi_settings">
          <h4 class="w-100 mt-1">ROIs &#9776;</h4>
        </button>
      </div>
      <div id="roi_settings" class="collapse mb-3 show roi_input">
        <!-- roi info -->
        <div id="roi_info_img_" class="mt-1 ref_rois">
          <span class="badge-secondary badge col-12">
            <button class="btn btn-secondary btn-block" data-bs-toggle="collapse" data-bs-target="#rois_img_"
              aria-expanded="true" aria-controls="rois_img_">
              <h5 class="col-12 mt-1">ROIs</h5>
            </button>
            <div id="rois_img_" class="collapse">
              <div class="row text-center mx-auto">
                <button id="import_ann_" class="btn btn-block btn-success import_ann col">
                  Import Rois From
                </button>
              </div>
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Image-Set</span>
                  </div>
                  <input id="import_ann_is_" type="Number" min="1" class="form-control col" placeholder="" />
                </div>
              </div>
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Image-Position</span>
                  </div>
                  <input id="import_ann_ip_" type="Number" min="1" class="form-control col" placeholder="" />
                </div>
              </div>
              <div class="row text-center mx-auto">
                <div class="input-group">
                  <div class="input-group-prepend col-6 px-0 mx-0">
                    <span class="input-group-text col-12">Stack-Position</span>
                  </div>
                  <input id="import_ann_sp_" type="Number" min="1" class="form-control col" placeholder="" />
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
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>
