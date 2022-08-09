<template>
<div class="container h-100">
  <div class="row justify-content-center align-items-center h-100">
    <div class="col-5 my-auto">
      <form class="form-horizontal" method="post" id="study_data" action="">
        <div class="input-group row mx-auto">
          <label class="input-group-text col-3">Username</label>
          <input class="form-control form-control" name="username" id="username" placeholder="username"
             value="" required>
        </div>

        <div class="input-group row mx-auto">
          <label class="input-group-text col-3">Password</label>
          <input class="form-control form-control" type="password" name="password" id="password" placeholder="password">
        </div>

        <div class="input-group mx-auto">
          <label class="input-group-text col-3">Type</label>
          <select class="form-select" name="access_level" id="access_level">
            <option value=""></option>
          </select>
        </div>

        <div class="row mx-auto mt-2">
          <input class="btn-secondary btn" value="update profile">
        </div>

      </form>
    </div>
  </div>
</div></template>

<script>
export default {

}
</script>

<style>

</style>
