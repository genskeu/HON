<template>
  <div class="accordion mt-4 mb-4">
    <div class="accordion-item bg-dark">
      <!-- header -->
      <div class="row">
        <div class="col-2 my-auto mx-auto">
          <button class="btn btn-lg btn-dark" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
            :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
          </button>
        </div>

        <div class="col-10 my-auto pr-5">
          <h1 class="accordion-header" id="imgset_settings_title">
            <button class="primary-accordion accordion-button show" type="button" data-bs-toggle="collapse"
              data-bs-target="#imgset_settings" aria-expanded="true" aria-controls="imgset_settings">
              <strong>Image-Sets &#9776;</strong>
            </button>
            <div v-if="imgsets.length > 0" class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
              title="">
              <label class="input-group-text bg-dark text-white border-0">Displayed</label>
              <select class='form-select border-0' v-model="imgsetDisplayed">
                <option :value="undefined"></option>
                <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position + 1 }}
                </option>
              </select>
              <label class="input-group-text  bg-dark text-white border-0">/{{ imgsets.length }}</label>
            </div>
          </h1>
        </div>
      </div>

      <!-- content -->
      <div id="imgset_settings" class="show accordion-collapse accordion">
        <!-- manual creation -->
        <manual-creation class="accordion-item"></manual-creation>
        <!-- auto creation -->
        <auto-creation class="accordion-item"></auto-creation>
      </div>
    </div>
  </div>
</template>

<script>
import { Popover } from 'bootstrap'
import manualCreation from '@/components/studyDesign/imgsetDesign/manualCreation.vue'
import autoCreation from '@/components/studyDesign/imgsetDesign/autoCreation.vue'

export default {
  name: 'ImgsetControl',
  components: {
    manualCreation,
    autoCreation
  },
  data () {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'This section controls the images displayed to users during a study. Images displayed simultaneously are called an Image-Set. Image-Sets can be created manually (one by one) using the Manual-Creation section or automatically using the Auto-Creation Menu.'
    }
  },
  computed: {
    imgsets () {
      return this.$store.getters['currentStudy/imgsets']
    },
    imgsetDisplayed: {
      get () {
        const imageSet = this.$store.getters['currentStudy/imgsetDisplayed']
        return imageSet
      },
      set (imgset) {
        this.$store.commit('currentStudy/imgsetDisplayed', imgset)
      }
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    },
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
  mounted () {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    Array.from(popoverTriggerList).map(popoverTriggerEl => new Popover(popoverTriggerEl))
  }
}
</script>

<style>
</style>
