<template>
  <!-- viewport info -->
  <div>
    <div class="row mx-auto">
      <button class="input-group-text " data-bs-toggle="collapse" :data-bs-target= "'#' + id"
        aria-expanded="true" :aria-controls="id">
        <h5 class="mx-auto">{{heading}}</h5>
      </button>
    </div>

    <div :id="id" class="collapse">
      <symetric-ROI v-for="uuid in Object.keys(EllipticalRois)" :key="uuid" :uuid="uuid" :target-viewer="this.targetViewer" :tool-name="'EllipticalRoi'"></symetric-ROI>
    </div>

    <div :id="id" class="collapse">
      <symetric-ROI v-for="uuid in Object.keys(RectangleRois)" :key="uuid" :uuid="uuid" :target-viewer="this.targetViewer" :tool-name="'RectangleRoi'"></symetric-ROI>
    </div>
  </div>
    <!--ROIs old-->
<!--     <div id="roi_settings_container" class="w-100 mb-1" title="The ROIs section shows the annotation coordinates drawn on each image.
                    ROIs can be drawn on images to define the ground truth in LROC and FROC studies.">
      <div class="row mx-auto roi_input">
        <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#roi_settings"
          aria-expanded="true" aria-controls="roi_settings">
          <h4 class="w-100 mt-1">ROIs &#9776;</h4>
        </button>
      </div>
      <div id="roi_settings" class="collapse mb-3 show roi_input">
        roi info
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
                <button id=overlap class="btn btn-primary overlap">overlap</button>
              </div>
            </div>
          </span>
        </div>
      </div>
    </div> -->
</template>

<script>
import symetricROI from '@/components/dicomViewer/ToolsAnnotationControl/symetricROI.vue'

export default {
  props: {
    targetViewer: Number
  },
  components: {
    symetricROI
  },
  data () {
    return {
    }
  },
  computed: {
    id () {
      return 'annotationControl_' + this.targetViewer
    },
    heading () {
      return 'Viewer ' + (this.targetViewer + 1)
    },
    EllipticalRois () {
      return this.$store.getters['imageViewers/EllipticalRois'](this.targetViewer)
    },
    RectangleRois () {
      return this.$store.getters['imageViewers/RectangleRois'](this.targetViewer)
    },
    CircleRois () {
      return this.$store.getters['imageViewers/CircleRois'](this.targetViewer)
    }
  }
}
</script>

<style>

</style>
