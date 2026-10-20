<template>
  <div class="row mx-auto">
      <h4 class="mx-auto" style="text-align:center;">
          <button class="btn btn-success vote_button mx-auto" @click="saveResult" :disabled="isLoading">{{this.buttonLabel}}</button>
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
  scales () {
    return this.$store.getters['currentStudy/scales']
  },
  textFields () {
    return this.$store.getters['currentStudy/textFields']
  },
  scaleInputs () {
    return this.$store.getters['studyInput/scaleInputs']
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
  },
  isLoading () {
    return this.$store.getters['loadingState/isLoading']
  },
  textInputs () { 
    return this.$store.getters['studyInput/textInputs'] 
  },
},
methods: {
  saveResult () {
    if (this.isLoading) {
      return
    } else {
      // get viewer id
      // get displayed imagestacks incl viewport settings (ww, wc ...) and tool states from store
      const imgset = this.imgsetInput
      // get scale data
      // sent data to backend via axios
      const stackIndex = this.refimageViewers.length + this.viewerIndex
      const stackPicked = imgset.stacks[stackIndex]
      // check all scales are filled in
      var emptyScale = this.scaleInputs.find(scaleInput => scaleInput.value === null)
      if (emptyScale) {
        alert('Scales empty: ' + emptyScale.name)
        return
      }
      // all text inputs must be filled
      var emptyTextInput = this.textInputs.find(textInput => textInput.value === null || textInput.value === '')
      if (emptyTextInput) {
        alert('Text input empty: ' + (emptyTextInput.text || ('Field ' + (this.textInputs.indexOf(emptyTextInput) + 1))))
        return
      }
      if (!this.checkLabeledAnnsPresent(stackPicked)) {
        return
      }
      // format for database
      // old: multiple values for one scaleInput possible (FROC, LROC)
      // new: each scaleInput has only one value and uuid 
      const scaleInputsDB = {}
      this.scaleInputs.forEach((scaleInput, index) => {
        const value = scaleInput.value
        const scaleName = 'Scale ' + (index + 1) + ' ' + scaleInput.name
        scaleInputsDB[scaleName] = { values: [value], uuids: [null] }
      })   
      const textInputDB = {}
      this.textInputs.forEach((textInput, i) => {
        const value = textInput.value
        const name = 'Textinput ' + (i + 1) + ' ' + textInput.name
        textInputDB[name] = { values: [value], uuids: [null] }
      })
      const payload = {
        imgset_id: this.imgsetDisplayed.id,
        picked_stack: stackPicked,
        stacks_displayed: imgset.stacks,
        scale_input: { ...scaleInputsDB, ...textInputDB }
      }

      this.$store.dispatch('studyInput/saveResult', payload)
    }
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
  },
  nextImgsetSpace (e) {
    if (e.code === 'Space') {
        this.saveResult()
      }
  },
  nextImgsetNumber (e) {
    const isNumber = /^[0-9]$/.test(e.key)
    if (e.key - 1 == this.viewerIndex && isNumber ){
      this.saveResult()
    }
  }
},
created () {
  // add event listener for space key if viewer number is 1
  // add event listener for number key if viewer number is more than 1 and no scales are present
  if (this.imageViewers.length === 1) {
    document.addEventListener('keydown', this.nextImgsetSpace)
  } else if (this.scales.length === 0 && this.textFields.length === 0) {
    document.addEventListener('keydown', this.nextImgsetNumber)
  }
},
unmounted () {
  document.removeEventListener('keydown', this.nextImgsetSpace)
  document.removeEventListener('keydown', this.nextImgsetNumber)
}
}
</script>

<style>

</style>
