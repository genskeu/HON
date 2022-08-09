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
    <div id="tools" class="collapse">
      <span class="badge bg-secondary w-100">
        <h4 class="">Mousekeys</h4>
      </span>
      <div v-for="tool in Object.keys(toolsMousekeys)" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="toolsMousekeys[tool]" v-model="toolsParticipant"/>
              {{tool}}
          </div>
        </div>
      </div>

      <span class="badge bg-secondary w-100">
        <h4 class="">Mousewheel</h4>
      </span>
      <div v-for="tool in Object.keys(toolsMousewheel)" :key="tool" class="input-group text-center mx-auto">
        <div class="input-group-prepend text-dark w-100">
          <div class="input-group-text w-100">
            <input type="checkbox" class="mr-3" id="" name="toolsCheck" :value="toolsMousewheel[tool]" v-model="toolsParticipant"/>
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
    toolsMousekeys: {
      get () {
        const tools = this.$store.getters['imageViewers/toolsMousekeys']
        var toolsParticipant = {}
        Object.keys(tools).forEach(tool => {
          toolsParticipant[tools[tool]] = { cs_name: tool, key_binding: null, settings: null }
        })
        return toolsParticipant
      }
    },
    toolsParticipant: {
      get () {
        const tools = this.$store.getters['openStudy/tools']
        return tools
      },
      set (tools) {
        this.$store.commit('openStudy/tools', tools)
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
  }
}
</script>

<style>

</style>
