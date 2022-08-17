<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{this.title}}</h5>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mx-auto spinner-border text-primary" role="status" style="width: 5rem; height: 5rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="modal-footer">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    title: String,
    text: String,
    loading: Boolean,
    showCloseBtn: Boolean
  },
  data () {
    return {
    }
  }
}
</script>

<style>

</style>
