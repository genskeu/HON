<template>
  <div
    id="login-modal"
    tabindex="-1"
    aria-hidden="true"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 w-full md:inset-0 h-modal md:h-full animate-fade-in"
  >
    <div class="relative p-4 w-full max-w-md h-full md:h-auto">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow">
        <div class="flex justify-end p-2">
          <button
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg p-1.5 ml-auto inline-flex items-center"
            data-modal-toggle="login-modal"
          >
            <i class="bx bx-x"> </i>
          </button>
        </div>
        <form class="px-6 pb-4 space-y-6 lg:px-8 sm:pb-6 xl:pb-8" action="#">
          <h3 class="text-xl font-medium text-gray-900">Sign in</h3>
          <div>
            <label
              for="email"
              class="flex mb-2 text-sm font-medium text-gray-900"
              >Your email</label
            >
            <input
              id="email"
              type="email"
              name="email"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary focus:border-ring-primary block w-full p-2.5"
              placeholder="name@company.com"
              required
            />
          </div>
          <div>
            <label
              for="password"
              class="flex mb-2 text-sm font-medium text-gray-900"
              >Your password</label
            >
            <input
              id="password"
              type="password"
              name="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-ring-primary block w-full p-2.5"
              required
            />
          </div>
          <div class="flex justify-between">
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  id="remember"
                  aria-describedby="remember"
                  type="checkbox"
                  class="w-4 h-4 bg-gray-50 rounded border border-gray-300 focus:ring-2 focus:ring-primary"
                  required
                />
              </div>
              <div class="ml-3 text-sm">
                <label for="remember" class="font-medium text-gray-900"
                  >Remember me</label
                >
              </div>
            </div>
            <a href="#" class="text-sm text-primary hover:underline"
              >Lost Password?</a
            >
          </div>
          <default-button
            type="submit"
            size="small"
            >Login to your account
          </default-button>
          <div class="flex text-sm font-medium text-gray-500">
            Not registered?
            <a href="#" class="pl-1 text-primary hover:underline">Create account</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultButton from "@/components/layout/DefaultButton.vue";

export default {
  name: "LoginModal",
  components: {
    DefaultButton,
  },
};
</script>
