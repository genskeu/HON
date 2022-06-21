<template>
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
</template>

<script>
export default {

}
</script>

<style>

</style>