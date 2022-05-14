<template>
  <div class="container">
        <div class="row mx-auto">
            <form action="" method="get">
                <input type="submit" class="btn btn-secondary mr-2" value="Access Study" data-toggle="tooltip"
                    data-placement="left"
                    title="Access any study for which you have the login. This functionality was included for study-admins for testing purposes.">
            </form>
            <form action="" method="get">
                <input type="submit" class="btn btn-success" value="Create New Study" data-toggle="tooltip"
                    data-placement="left" title="Study creation is a 3 step process:
      1) Study name, access password, and description are selected.
      2) Study images are uploaded.
      3) Study design is finalized by customizing layout, image display and annotation options.">
            </form>
        </div>
        <div class="row mx-auto mt-2">
            <button type="button" class="btn btn-dark btn-block" data-toggle="collapse" data-target="#studies_ov"
                aria-expanded="true" aria-controls="studies_ov">
                <h4 class="col-12 mt-1">Studies &#9776;</h4>
            </button>
        </div>
        <div class="row mx-auto collapse show" id="studies_ov">
            <table class="table table-hover">
                <thead class="thead-light">
                    <tr>
                        <th>Name</th>
                        <th>Study Id</th>
                        <th>Created</th>
                        <th>Modified</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="align-middle"></td>
                        <td class="align-middle"></td>
                        <td class="align-middle"></td>
                        <td class="align-middle"></td>
                        <td>
                            <form class="" action="" method="get">
                                <button class="btn-secondary btn-sm">modify</button>
                            </form>
                        </td>
                        <td>
                            <button class="btn-danger btn-sm" onclick="">delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
  </div>
</template>

<script>
export default {
  name: 'StudyOverview'
}
</script>

<style>
</style>
