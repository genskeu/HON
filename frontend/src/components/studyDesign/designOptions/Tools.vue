<template>
  <div>
    <!-- tool settings -->
    <div class="row mx-auto mt-1">
      <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#tools" aria-expanded="true"
        aria-controls="tools" title="Tools define DICOM viewer and annotation tools that are made available to participants
                    (e.g., scrolling, windowing, rectangular, elliptical or free-hand ROIs).">
        <h5 class="mt-1 col-12">Tools</h5>
      </button>
    </div>
    <div id="tools" class="collapse mt-1">
      <div class="bg-secondary w-100">
        Viewer Settings Mousekeys
      </div>
      <div v-for="(label, tool) in viewerSettingToolsMousekeys" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="label" v-model="toolsParticipant" />
            {{tool}}
          </div>
        </div>
      </div>
      <div class="bg-secondary w-100 mt-1">
        Annotations Mousekeys
      </div>
      <div v-for="(label, tool) in annotationToolsMousekeys" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="label" v-model="toolsParticipant" />
            {{tool}}
            <button v-if="label.cs_name !== 'Eraser'" class="pull-right ml-auto" data-bs-toggle="collapse"
              :data-bs-target="'#' + label.cs_name + 'Settings'" aria-expanded="true"
              :aria-controls="label.cs_name + 'Settings'">Settings</button>
          </div>
        </div>
        <!-- tool setting, only implemented interface for annotaton tools -->
        <div v-if="label.cs_name !== 'Eraser'" class="mx-auto collapse" :id="label.cs_name + 'Settings'">
          <div class="input-group mx-auto">
            <label class="input-group-text w-35">Length/ Diameter</label>
            <input :value="label.settings.size" @change="(event) => updateToolSettings(event, label.cs_name, 'size')"
              type="Number" step="any" min="0" class="form-control" placeholder="size in px" />
          </div>
          <div class="input-group mx-auto">
            <label class="input-group-text w-35">Number</label>
            <input :value="label.settings.minNumber"
              @change="(event) => updateToolSettings(event, label.cs_name, 'minNumber')" type="Number" step="any"
              min="0" class="form-control" placeholder="min" />
              <label class="input-group-text">-</label>
            <input :value="label.settings.maxNumber"
              @change="(event) => updateToolSettings(event, label.cs_name, 'maxNumber')" type="Number" step="any"
              class="form-control wc " placeholder="max" />
          </div>
          <div v-if="label.settings.maxNumber && label.settings.maxNumber > label.settings.minNumber">
            <div  class="row mx-auto">
            <button class="input-group-text " data-bs-toggle="collapse" :data-bs-target="'#labels_' + label.cs_name"
              aria-expanded="true" :aria-controls="'#labels_' + label.cs_name">
              <h5 class="mx-auto">Annotation Names</h5>
            </button>
          </div>
          <div :id="'labels_' + label.cs_name" class="collapse show">
            <div v-for="i in Number(label.settings.maxNumber)" :key="i" class="input-group mx-auto">
              <label class="input-group-text w-25">{{i}}</label>
              <input :value="label.settings.labels[i-1]" @change="(event) => updateToolLabel(event, label.cs_name, i-1)" class="form-control" type="text" />
            </div>
          </div>
          </div>
        </div>
      </div>

      <div class="bg-secondary w-100 mt-1">
        Segmentations Mousekeys
      </div>
      <div v-for="(label, tool) in segmentationToolsMousekeys" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="label" v-model="toolsParticipant" />
            {{tool}}
          </div>
        </div>
      </div>

      <div class="bg-secondary w-100 mt-1">
        <h4 class="">Viewer Settings Mousewheel</h4>
      </div>
      <div v-for="(label, tool) in viewerToolsMousewheelSettings" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="label" v-model="toolsParticipant" />
            {{tool}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    annotationToolsMousekeys () {
      return this.$store.getters['currentStudy/annToolsMousekeysSettings']
    },
    viewerSettingToolsMousekeys () {
      return this.$store.getters['currentStudy/viewerToolsMousekeysSettings']
    },
    segmentationToolsMousekeys () {
      return this.$store.getters['currentStudy/segToolsMousekeysSettings']
    },
    viewerToolsMousewheelSettings () {
      return this.$store.getters['currentStudy/viewerToolsMousewheelSettings']
    },
    toolsParticipant: {
      get () {
        return this.$store.getters['currentStudy/tools']
      },
      set (tools) {
        this.$store.commit('currentStudy/tools', tools)
      }
    },
    toolsMousewheel () {
      const tools = this.$store.getters['imageViewers/toolsMousewheel']
      var toolsParticipant = {}
      Object.keys(tools).forEach(tool => {
        toolsParticipant[tools[tool]] = { cs_name: tool, key_binding: null, settings: null }
      })
      return toolsParticipant
    }
  },
  methods: {
    updateToolSettings (event, csName, propName) {
      const payload = { csName: csName, value: event.target.value, propName: propName }
      this.$store.commit('currentStudy/toolSettings', payload)
    },
    updateToolLabel (event, csName, labelIndex) {
      const payload = { csName: csName, value: event.target.value, labelIndex: labelIndex }
      this.$store.commit('currentStudy/toolLabel', payload)
    }
  }
}
</script>

<style>
</style>
