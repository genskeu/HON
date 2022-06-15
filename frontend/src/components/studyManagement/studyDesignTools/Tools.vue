<template>
  <div>
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
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>