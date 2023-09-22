<template>
    <b-container class="bv-example-row bv-example-row-flex-cols">
        <b-row>
            <b-col style="padding-top: 200px" offset-md="4" md="4" align-self="center">
                <b-navbar variant="faded" style="justify-content: center" type="light">
                    <b-navbar-brand tag="h1" class="mb-0">Welcome to the Library</b-navbar-brand>
                </b-navbar>
                <b-form @submit="onSubmit">
                    <b-form-group
                        id="input-group-1"
                        label="Username"
                        label-for="input-1"
                        description="Please use the provided username to login"
                    >
                        <b-form-input
                            id="input-1"
                            v-model="form.username"
                            type="email"
                            placeholder="Enter your username or email"
                            required
                        ></b-form-input>
                    </b-form-group>

                    <b-form @submit.stop.prevent>
                        <label for="text-password">Password</label>
                        <b-form-input
                            @keyup.enter="onSubmit"
                            v-model="form.password"
                            type="password"
                            id="text-password"
                        ></b-form-input>
                    </b-form>

                    <b-button type="submit" style="margin: 24px 0; width: 100%" variant="primary">Submit</b-button>
                </b-form>

                <b-alert
                    :show="dismissCountDown"
                    dismissible
                    variant="warning"
                    @dismissed="dismissCountDown = 0"
                    @dismiss-count-down="countDownChanged"
                >
                    Invalid username/password. Please try again
                </b-alert>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    data() {
        return {
            form: {
                username: '',
                password: '',
            },
            show: true,
            dismissSecs: 5,
            dismissCountDown: 0,
        };
    },
    methods: {
        async onSubmit(event) {
            event.preventDefault();
            var data = new URLSearchParams();
            data.append('username', this.form.username);
            data.append('password', this.form.password);
            try {
                let response = await this.$auth.loginWith('local', { data });
                if (response.status === 200) {
                    this.$auth.setUser(response.data.name);
                    this.$router.push({ path: '/' });
                }
            } catch (err) {
                this.dismissCountDown = this.dismissSecs;
            }
        },
    },
};
</script>
