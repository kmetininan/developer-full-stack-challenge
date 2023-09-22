<template>
    <div>
        <b-navbar toggleable="lg" type="light">
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item :class="$route.path === '/' && 'highlight'" href="/">Authors</b-nav-item>
                    <b-nav-item :class="$route.path === '/books' && 'highlight'" href="/books">Books</b-nav-item>
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-nav-item right>
                        <!-- Using 'button-content' slot -->
                        <template #button-content>
                            <div v-if="$auth.loggedIn">
                                {{ 'User' || $auth.user || 'User' }}
                            </div>
                        </template>
                    </b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <slot />
    </div>
</template>

<script>
export default {
    methods: {
        logout() {
            window.localStorage.clear();
            var cookies = document.cookie.split(';');
            // set 1 Jan, 1970 expiry for every cookies
            for (var i = 0; i < cookies.length; i++)
                document.cookie = cookies[i] + '=;expires=' + new Date(0).toUTCString();
            this.$router.push({ path: '/login' });
        },
    },
};
</script>
<style scoped>
.highlight a {
    font-weight: bold;
    color: #007bff !important;
}
</style>
