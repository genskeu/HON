<template>
<div class="container">
  <div class="row mx-auto mb-4">
    <form action="" method="get">
      <input class="btn btn-success mr-2" value="Create New User">
    </form>
  </div>

  <div class="mx-auto">
    <button class="btn btn-secondary btn-block" data-toggle="collapse" data-target="#table{{i}}"
      aria-expanded="false" aria-controls="table">
      <h5 class="col-12 mt-1"></h5>
    </button>
    <div id="table" class="row mx-auto overflow-auto show" style="max-height: 300px;">
      <table class="table table-hover">
        <thead class="thead-dark">
          <tr>
            <!-- col-3 for width of cloumns does not work in chrome for tables use style="width: 25%" -->
            <th style="width: 19%">Name</th>
            <th style="width: 8%">Id</th>
            <th style="width: 25%">Created</th>
            <th style="width: 16%"> </th>
            <th style="width: 16%"></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="align-middle"></td>
            <td class="align-middle"></td>
            <td class="align-middle"></td>
            <td class="align-middle">
              <form class="" action="" method="get">
                <button class="btn-secondary btn-sm">modify</button>
              </form>
            </td>
            <td class="align-middle">
              <button class="btn-danger btn-sm" onclick="">delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
