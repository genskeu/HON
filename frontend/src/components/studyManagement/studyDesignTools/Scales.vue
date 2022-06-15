<template>
  <div>
              <!-- scales -->
          <div
            class="row mx-auto mt-1"
            title="Scales can be customized and are displayed to participants throughout studies."
          >
            <button
              class="btn btn-secondary col-12"
              data-bs-toggle="collapse"
              data-bs-target="#scales_container"
              aria-expanded="true"
              aria-controls="scales_container"
            >
              <h5 class="mt-1">Scale(s)</h5>
            </button>
          </div>
          <div id="scales_container" class="collapse">
            <div class="row mx-auto">
              <button class="btn btn-success btn-block col" id="add_scale">
                add scale
              </button>
            </div>

            <div id="scales" class="mt-1">
              <!-- templetate to create new scales using js -->
              <div
                id="scale_"
                class="mt-1 scale_template"
                style="display: none"
              >
                <span class="badge badge-light w-100 mt-1">
                  <h6 id="scale_heading_" class="mt-1 scale_heading">Scale</h6>
                </span>
                <!-- admin view to define scale -->
                <div class="mx-auto scale_view_admin" id="scale_view_admin_">
                  <div
                    class="row mx-auto scale_text_admin"
                    id="scale_text_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Text</span>
                      </div>
                      <textarea
                        id="scale_text_input_"
                        class="form-control scale_text_input"
                      ></textarea>
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_min_admin"
                    id="scale_min_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Start</span>
                      </div>
                      <input
                        class="form-control scale_min_input"
                        min="-100"
                        max="100"
                        type="number"
                        id="scale_min_input_"
                        placeholder="min"
                        value=""
                      />
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_max_admin"
                    id="scale_max_admin_"
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">End</span>
                      </div>
                      <input
                        class="form-control scale_max_input"
                        min="-100"
                        max="100"
                        type="number"
                        id="scale_max_input_"
                        placeholder="max"
                        value=""
                      />
                    </div>
                  </div>
                  <div
                    class="row mx-auto scale_type_admin"
                    id="scale_type_admin_"
                    title="Can be left blank for most studies except for FROC designs,
                    where a scale needs to be repeated each time a new roi is drawn."
                  >
                    <div class="input-group">
                      <div class="input-group-prepend col-4 px-0 mx-0">
                        <span class="input-group-text col-12">Type</span>
                      </div>

                      <select
                        id="scale_type_input_"
                        class="custom-select scale_type_input"
                      >
                        <option value=""></option>
                        <option value=""></option>
                      </select>
                    </div>
                  </div>
                  <button
                    class="btn btn-danger btn-block scale_rm"
                    id="scale_rm_"
                  >
                    rm scale
                  </button>
                </div>
                <!-- participant view of scale -->
                <div class="mx-auto mb-3 scale_view_user" id="scale_view_user_">
                  <div class="row mx-auto justify-content-center">
                    <div
                      id="scale_text_"
                      class="col scale_text"
                      style="white-space: pre-wrap; text-align: center"
                    ></div>
                  </div>
                  <div
                    class="row mx-auto justify-content-center mt-1 scale_values"
                    id="scale_values_"
                    style="display: none"
                  ></div>
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
