<template>
<div class="container mt-4">
  <div class="mx-auto">
    <div v-for="(users, usertype) in userOverview" :key="usertype" id="table" class="row mx-auto overflow-auto show" style="max-height: 300px;">
      <table class="table table-hover">
                <thead class="thead-light">
                    <tr>
                        <th class="align-middle">Name</th>
                        <th class="align-middle">User Id</th>
                        <th class="align-middle">Created</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td class="align-middle">{{user.username}}</td>
                        <td class="align-middle">{{user.id}}</td>
                        <td class="align-middle">{{user.created}}</td>
                        <td>
                          <button @click="editUser(user.id)" class="btn-success btn">edit</button>
                        </td>
                        <td>
                        </td>
                        <td>
                            <button class="btn-danger btn" data-bs-toggle="modal" data-bs-target="#deleteUser" @click="setUserDelete(user)">delete
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
import router from '@/router'

export default {
  computed: {
    users () {
      return this.$store.getters['users/users']
    },
    studyAdmins () {
      return this.users.filter(user => user.access_level === 2)
    },
    studyParticipants () {
      return this.users.filter(user => user.access_level === 1)
    },
    userAdmins () {
      return this.users.filter(user => user.access_level === 3)
    },
    userOverview () {
      return {
        "Participants": this.studyParticipants,
        "Study Admins": this.studyAdmins,
        "User Admins": this.userAdmins
      }
    }
  },
  methods:{
    editUser (userId) {
      router.push('/user-management/edit-user/' + userId)
    },
  }
}
</script>

<style>

</style>
