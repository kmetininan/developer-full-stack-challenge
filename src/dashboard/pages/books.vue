<template>
    <pages-layout>
        <div>
            <b-container fluid class="bv-example-row">
                <b-row>
                    <b-col>
                        <b-row class="my-1">
                            <b-col span="12">
                                <b-form-input
                                    v-model="query"
                                    @keyup.enter="onSearch"
                                    placeholder="Search for your book"
                                    :type="search"
                                ></b-form-input>
                            </b-col>
                            <b-col>
                                <div>
                                    <b-button variant="primary" v-b-modal.modal-prevent-closing>Add book</b-button>

                                    <b-modal
                                        id="modal-prevent-closing"
                                        ref="modal"
                                        @show="resetModal"
                                        @hidden="resetModal"
                                        @ok="handleOk"
                                        hide-backdrop
                                        content-class="shadow"
                                        title="Add book"
                                    >
                                        <form ref="form" @submit.stop.prevent="handleSubmit">
                                            <b-form-group
                                                label="Name"
                                                label-for="name-input"
                                                invalid-feedback="Name is required"
                                                :state="nameState"
                                            >
                                                <b-form-input
                                                    id="name-input"
                                                    v-model="addBook.name"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>
                                            <b-form-group
                                                label="Page Count"
                                                label-for="pages-input"
                                                invalid-feedback="Name is required"
                                                :state="nameState"
                                            >
                                                <b-form-input
                                                    id="pages-input"
                                                    v-model="addBook.pages_count"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>
                                            <b-form-group
                                                label="Author"
                                                label-for="author-input"
                                                invalid-feedback="Author is required"
                                                :state="nameState"
                                            >
                                                <treeselect
                                                    id="author-input"
                                                    v-model="value"
                                                    @input="updateValue"
                                                    :options="authors"
                                                />
                                            </b-form-group>
                                        </form>
                                    </b-modal>
                                </div>

                                <div>
                                    <b-modal
                                        id="modal-prevent-closing-edit"
                                        ref="modal"
                                        @hidden="resetModal"
                                        @ok="handleEditSubmit"
                                        hide-backdrop
                                        content-class="shadow"
                                        title="Edit book"
                                    >
                                        <form ref="form" @submit.stop.prevent="handleEditSubmit">
                                            <b-form-group
                                                label="Name"
                                                label-for="name-input"
                                                invalid-feedback="Name is required"
                                                :state="nameState"
                                            >
                                                <b-form-input
                                                    id="name-input"
                                                    v-model="editBook.name"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>
                                            <b-form-group
                                                label="Page Count"
                                                label-for="pages-input"
                                                invalid-feedback="Name is required"
                                                :state="nameState"
                                            >
                                                <b-form-input
                                                    id="pages-input"
                                                    v-model="editBook.pages_count"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>
                                            <b-form-group
                                                label="Author"
                                                label-for="author-input"
                                                invalid-feedback="Author is required"
                                                :state="nameState"
                                            >
                                                <treeselect
                                                    id="author-input"
                                                    v-model="editBook.author_id"
                                                    @input="updateValue"
                                                    :options="authors"
                                                />
                                            </b-form-group>
                                        </form>
                                        <template #modal-footer="{ ok }" style="display: block">
                                            <b-button size="md" variant="outline-danger" @click="deleteBook()">
                                                Delete
                                            </b-button>
                                            <b-button style="float: right" size="md" variant="success" @click="ok()">
                                                Save
                                            </b-button>
                                        </template>
                                    </b-modal>
                                </div>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>
                <b-row style="margin-top: 24px">
                    <b-col>
                        <b-table
                            :bordered="bordered"
                            :items="books"
                            :select-mode="single"
                            :fields="bookFields"
                            :head-variant="light"
                            selectable
                            responsive="sm"
                            ref="selectableTable"
                            @row-selected="onRowSelected"
                        ></b-table
                    ></b-col>
                </b-row>
            </b-container>
        </div>
    </pages-layout>
</template>

<script>
import Treeselect from '@riophae/vue-treeselect';
// import the styles
import '@riophae/vue-treeselect/dist/vue-treeselect.css';
import PagesLayout from '../layouts/pages.vue';
export default {
    components: {
        PagesLayout,
        Treeselect,
    },
    data() {
        return {
            value: null,
            // define options
            authors: [],
            bookFields: [
                'name',
                {
                    key: 'author.name',
                    label: 'Author',
                },
                'pages_count',
            ],
            bordered: true,
            query: '',
            addBook: {
                name: '',
                pages_count: 0,
                author_id: 0,
            },
            nameState: null,
            books: [],
            editBook: {
                id: 0,
                name: '',
                pages_count: 0,
                author_id: 0,
            },
        };
    },

    methods: {
        getAuthors: async function () {
            const response = await this.$axios.get(`/authors`);
            const authors = response.data;
            const options = [];
            for (let i of authors) options.push({ id: i['id'], label: i['name'] });
            this.authors = options;
        },
        getBooks: async function () {
            const response = await this.$axios.get(`/books?q=${this.query}`);
            this.books = response.data;
        },
        deleteBook: async function () {
            const response = await this.$axios.delete(`/books/${this.editBook.id}`);
            this.getBooks();
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing-edit');
                this.clearSelected();
            });
        },
        saveBook: async function () {
            const response = await this.$axios.post('/books', {
                name: this.addBook.name,
                pages_count: this.addBook.pages_count,
                author_id: this.addBook.author_id,
            });
            this.getBooks();
        },
        saveChangesBook: async function () {
            const response = await this.$axios.put(`/books/${this.editBook.id}`, {
                name: this.editBook.name,
                pages_count: this.editBook.pages_count,
                author_id: this.editBook.author_id,
            });
            this.getBooks();
        },
        onSearch: function (event) {
            this.query = event.currentTarget.value;
            this.getBooks();
        },
        checkFormValidity: function () {
            const valid = this.$refs.form.checkValidity();
            this.nameState = valid;
            return valid;
        },
        resetModal: function () {
            this.addBook = {
                name: '',
                pages_count: 0,
                author_id: 0,
            };
            this.nameState = null;
            this.clearSelected();
        },
        handleOk: function (bvModalEvent) {
            // Prevent modal from closing
            bvModalEvent.preventDefault();
            // Trigger submit handler
            this.handleSubmit();
        },
        handleEdit: function (bvModalEvent) {
            // Prevent modal from closing
            bvModalEvent.preventDefault();
            // Trigger submit handler
            this.handleEditSubmit();
        },
        handleSubmit: function () {
            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }
            this.saveBook();
            // Hide the modal manually
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing');
            });
        },
        handleEditSubmit: function () {
            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }
            this.saveChangesBook();
            // Hide the modal manually
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing-edit');
                this.clearSelected();
            });
        },
        onRowSelected: function (items) {
            if (items.length > 0) {
                this.editBook = {
                    id: items[0].id,
                    name: items[0].name,
                    pages_count: items[0].pages_count,
                    author_id: items[0].author.id,
                };
                this.$bvModal.show('modal-prevent-closing-edit');
            }
        },
        clearSelected: function () {
            this.$refs.selectableTable.clearSelected();
        },
        addNewBook: function () {
            const books = this.addBook.books.slice();
            const newBook = {
                name: '',
                id: books.length + 1,
                pages_count: 0,
            };
            books.push(newBook);
            this.addBook.books = books;
        },
        updateValue(event) {
            this.addBook.author_id = event;
        },
    },
    fetch() {
        this.getBooks();
        this.getAuthors();
    },
};
</script>
