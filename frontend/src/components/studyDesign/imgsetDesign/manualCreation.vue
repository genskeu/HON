<template>
    <div>
        <div class="row">
            <div class="col-2 my-auto mx-auto">
                <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
                    :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
                </button>
            </div>

            <div class="col-10">
                <h2 class="accordion-header" id="general_settings_title">
                    <button id="acc-btn-man-imgsets" class="accordion-button" type="button" data-bs-toggle="collapse"
                        data-bs-target="#images_create_man" aria-expanded="true" aria-controls="images_create_man">
                        Manual-Creation
                    </button>
                </h2>
            </div>
        </div>
        <div class="collapse accordion-collapse show" id="images_create_man">
            <div>
              <div v-if="imgsets.length > 0" class="input-group mx-auto mb-1" data-toggle="tooltip" data-placement="left"
                    title="">
                    <label class="input-group-text bg-gray-300">Set Displayed</label>
                    <select class='form-select' v-model="imgsetDisplayed">
                        <option :value="undefined"></option>
                        <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position + 1 }}
                        </option>
                    </select>
                    <label class="input-group-text bg-gray-300">/{{ imgsets.length }}</label>
                </div>
                <div class="row mx-auto">
                    <button class="text-start btn btn-light input-group-text bg-gray-300" data-bs-toggle="collapse"
                        data-bs-target="#images_displayed" aria-expanded="true" aria-controls="images_displayed">
                        <div class="mr-auto">Images displayed</div>
                    </button>
                </div>

                <div id="images_displayed" class="collapse show">
                    <div v-if="refviewerNumb" class="input-group-text">
                        <h5 class="mx-auto">Reference-Images</h5>
                    </div>
                    <div v-for="index in refviewerNumb" :key="index">
                        <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="refviewers">
                        </DicomViewerImageSelect>
                    </div>
                    <div v-if="refviewerNumb" class="input-group-text">
                        <h5 class="mx-auto">Images</h5>
                    </div>
                    <div v-for="index in viewerNumb" :key="index">
                        <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="viewers">
                        </DicomViewerImageSelect>
                    </div>
                </div>
                <!-- viewport settings -->
                <div id="viewport_settings_container" class="w-100 mt-1"
                    title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images. Each viewport can be controlled individually.">
                    <div class="row mx-auto">
                        <button class="text-start btn btn-light input-group-text bg-gray-300" data-bs-toggle="collapse"
                            data-bs-target="#viewport_settings" aria-expanded="true" aria-controls="viewport_settings">
                            <div class="mr-auto" id="imgset_btn">Viewer Settings</div>
                        </button>
                    </div>
                    <div id="viewport_settings" class="collapse">
                        <div v-if="refviewerNumb" class="input-group-text">
                            <h5 class="mx-auto">Reference-Images</h5>
                        </div>
                        <div id="" v-for="(viewer, index) in refimageViewers" :key="index">
                            <DicomViewportControl :target-viewer="index" viewer-type="refviewers">
                            </DicomViewportControl>
                        </div>
                        <div v-if="refviewerNumb" class="input-group-text">
                            <h5 class="mx-auto">Images</h5>
                        </div>
                        <div id="" v-for="(viewer, index) in imageViewers" :key="index">
                            <DicomViewportControl :target-viewer="index" viewer-type="viewers"></DicomViewportControl>
                        </div>
                    </div>
                </div>
                <div v-if="false" id="annotations_settings_container" class="w-100 mt-1" title="">
                    <div class="row mt-1 mx-auto">
                        <button class="btn bg-gray-300 col-12" data-bs-toggle="collapse"
                            data-bs-target="#annotation_settings" aria-expanded="true"
                            aria-controls="viewport_settings">
                            <h4 class="w-100 mt-1">Annotation Settings</h4>
                        </button>
                    </div>
                    <div id="annotation_settings" class="collapse">
                        <div id="" v-for="(viewer, index) in imageViewers" :key="index">
                            <ToolsAnnotationControl :target-viewer="index" viewer-type="viewers">
                            </ToolsAnnotationControl>
                        </div>
                    </div>
                </div>

                <div class="row mt-1">
                    <div class="input-group">
                        <button class="text-start btn-success btn col-9" title="add image-set to the end of the study"
                            @click.prevent="addImgset">Add Image-Set at Pos
                        </button>
                        <input class="form-control" type="Number" min="1" :max="imgsets.length + 1" step="1"
                            id="numb_refimg" v-model="imagesetAddPosition" />
                    </div>
                </div>
                <div v-if="imgsetDisplayed" class="row mx-auto">
                    <button value="update loaded imgset" class=" text-start imgset_btn btn-light btn" id="upd_imgset"
                        title="update currently selected image-set" @click.prevent="updateImgset">Update Image-Set
                    </button>
                </div>
                <div v-if="imgsetDisplayed" class="row mx-auto">
                    <button value="Delete Image-Set" class="text-start imgset_btn btn-danger btn" id="del_imgset"
                        title="delete currently selected image-set" @click.prevent="deleteImgset">Delete Image-Set
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'
import ToolsAnnotationControl from '@/components/dicomViewer/ToolsAnnotationControl.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'

export default {
  components: {
    DicomViewerImageSelect,
    ToolsAnnotationControl,
    DicomViewportControl
  },
  data () {
    return {
      imagesetAddPosition: 1,
      popoverTitle: 'Section Info',
      popoverText: 'This section can be used to create, modify and delete individual Image-Sets. Existing Image-Sets can be loaded via the "Set Displayed Menu". For each viewer an image can be selected using the "Images Displayed" dropdown menus. Settings such as image position, windowing and zoom level can be controlled via the "Viewer Settings" Menus.'
    }
  },
  computed: {
    stacks () {
      return this.$store.getters['currentStudy/stacks']
    },
    imgsets () {
      return this.$store.getters['currentStudy/imgsets']
    },
    viewerNumb () {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    refviewerNumb () {
      return this.$store.getters['currentStudy/refviewerNumb']
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    },
    imgsetDisplayed: {
      get () {
        const imageSet = this.$store.getters['currentStudy/imgsetDisplayed']
        return imageSet
      },
      set (imgset) {
        this.$store.commit('currentStudy/imgsetDisplayed', imgset)
      }
    }
  },
  watch: {
    imgsetDisplayed: {
      handler (newImgset) {
        // code could be moved to store to avoid duplication?
        if (newImgset) {
          const viewers = this.refimageViewers.concat(this.imageViewers)
          // itterate over viewers and display stack according to div_id
          // if no stack found reset stack to trigger viewer reset
          viewers.forEach((viewer, index) => {
            var stack = newImgset.image_stacks.find(stack => stack.div_id === 'dicom_img_' + index)
            if (stack === undefined) {
              stack = {
                cs_stack: {
                  imageIds: [],
                  currentImageIdIndex: Number
                },
                name: String,
                savedSegmentation: undefined,
                savedToolstate: undefined,
                savedViewport: undefined
              }
            }
            var viewertype = this.refimageViewers.includes(viewer) ? 'refviewers' : 'viewers'
            var viewerindex = this.refimageViewers.includes(viewer) ? index : index - this.refimageViewers.length
            const stackData = {
              stack_id: stack.stack_id,
              name: stack.name,
              stackDisplayed: stack.cs_stack,
              savedViewport: stack.viewport,
              savedToolstate: stack.tool_state,
              savedSegmentation: stack.seg_data,
              index: viewerindex,
              viewertype: viewertype
            }
            this.$store.commit('imageViewers/stackDisplayed', stackData)
          })
        } else {
          const emptyStack = {
            cs_stack: {
              currentImageIdIndex: Number,
              imageIds: []
            },
            name: String
          }
          const viewers = this.refimageViewers.concat(this.imageViewers)
          // itterate over viewers and display stack according to div_id
          // if no stack found reset stack to trigger viewer reset
          viewers.forEach((viewer, index) => {
            var viewertype = this.refimageViewers.includes(viewer) ? 'refviewers' : 'viewers'
            var viewerindex = this.refimageViewers.includes(viewer) ? index : index - this.refimageViewers.length
            const stackData = {
              name: emptyStack.name,
              stackDisplayed: emptyStack.cs_stack,
              index: viewerindex,
              viewertype: viewertype
            }
            this.$store.commit('imageViewers/stackDisplayed', stackData)
          })
        }
      }
    }
  },
  methods: {
    addImgset () {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imagesetAddPosition - 1
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/addImgset', payload)
    },
    updateImgset () {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imgsetDisplayed.position
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/updImgset', payload)
    },
    deleteImgset () {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imgsetDisplayed.position
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/delImgset', payload)
    }
  }
}
</script>

<style>

</style>
