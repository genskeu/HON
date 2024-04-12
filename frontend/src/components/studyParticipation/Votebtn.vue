<template>
    <div class="row mx-auto">
        <h4 class="mx-auto" style="text-align:center;">
            <button class="btn btn-success vote_button mx-auto" @click="saveResult">{{this.buttonLabel}}</button>
        </h4>
    </div>
</template>

<script>
import cornerstoneTools from 'cornerstone-tools'

export default {
  name: 'VoteBtn',
  props: {
    viewerIndex: Number
  },
  computed: {
    buttonLabel () {
      return this.$store.getters['currentStudy/buttonLabels']
    },
    scalesInput () {
      return this.$store.getters['currentStudy/scalesInput']
    },
    scalesInputDB () {
      return this.$store.getters['currentStudy/scalesInputDB']
    },
    imgsetDisplayed () {
      return this.$store.getters['currentStudy/imgsetDisplayed']
    },
    imgsetInput () {
      return this.$store.getters['imageViewers/getImgset']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    },
    toolsParticipant () {
      return this.$store.getters['currentStudy/tools']
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    }
  },
  methods: {
    saveResult () {
      // get viewer id
      // get displayed imagestacks incl viewport settings (ww, wc ...) and tool states from store
      const imgset = this.imgsetInput
      // get scale data
      // sent data to backend via axios
      const stackIndex = this.refimageViewers.length + this.viewerIndex
      const stackPicked = imgset.stacks[stackIndex]
      const payload = {
        imgset_id: this.imgsetDisplayed.id,
        picked_stack: stackPicked,
        stacks_displayed: imgset.stacks,
        scale_input: this.scalesInputDB
      }
      // check all scales are filled in
      var emptyScale = this.scalesInput.find(scaleInput => scaleInput.value === null)
      if (emptyScale) {
        alert('Scales empty: ' + emptyScale.name)
        return
      }
      if (!this.checkLabeledAnnsPresent(stackPicked)) {
        return
      }
      this.$store.dispatch('currentStudy/saveResult', payload)
    },
    // helper function to check if labeled tools are used in this study
    // ensure for all labeled tools measurments were taken
    labeledTools () {
      const toolsLabeld = this.toolsParticipant.filter(tool => tool.settings.labels !== undefined)
      var toolCsNames = []
      toolsLabeld.forEach((tool) => {
        tool.settings.labels.forEach(label => {
          toolCsNames.push(tool.cs_name + '-' + label)
        })
      })
      return toolCsNames
    },
    numbAnnsStack (stack, toolName) {
      const imageIds = stack.imageIds
      const toolState = imageIds.map((id) => {
        return cornerstoneTools.globalImageIdSpecificToolStateManager.getImageIdToolState(id, toolName)
      })
      const toolStateFiltered = toolState.filter((state) => state !== undefined)
      const lengthToolState = toolStateFiltered.reduce((length, state) => {
        return length + state.data.length
      }, 0)
      return lengthToolState
    },
    checkLabeledAnnsPresent (stack) {
      var allLabelsPresent = true
      this.labeledTools().forEach((labeldTool) => {
        const numbAnn = this.numbAnnsStack(stack, labeldTool)
        if (numbAnn === 0) {
          alert('Missing Measurement ' + labeldTool)
          allLabelsPresent = false
        }
      })
      return allLabelsPresent
    }
  },
  mounted () {
    // add event listener for space key if viewer number is 1
    // add event listener for number key if viewer number is more than 1 and no scales are present
    if (this.imageViewers.length === 1) {
      document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
          console.log('Space pressed')
          this.saveResult()
        }
      })
    } else if (this.scalesInput.length === 0) {
      document.addEventListener('keydown', (e) => {
        const isNumber = /^[0-9]$/.test(e.key)
        if (e.key - 1 == this.viewerIndex && isNumber ){
          this.saveResult()
        }
      })
    }
  }
}
</script>

<style>

</style>
