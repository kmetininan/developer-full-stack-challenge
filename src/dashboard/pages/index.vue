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
                                    placeholder="Search for your author"
                                    :type="search"
                                ></b-form-input>
                            </b-col>
                            <b-col>
                                <div>
                                    <b-button variant="primary" v-b-modal.modal-prevent-closing>Add author</b-button>

                                    <b-modal
                                        id="modal-prevent-closing"
                                        ref="modal"
                                        @show="resetModal"
                                        @hidden="resetModal"
                                        @ok="handleOk"
                                        hide-backdrop
                                        content-class="shadow"
                                        title="Add author"
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
                                                    v-model="addAuthor.name"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>

                                            <b-form-group
                                                label-cols-lg="12"
                                                label="Books"
                                                label-size="md"
                                                label-class=" pt-0"
                                                class="mb-0"
                                            >
                                                <b-row v-if="addAuthor.books.length > 0">
                                                    <b-col md="6">
                                                        <b-form-group
                                                            label="Book Name"
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="6">
                                                        <b-form-group
                                                            label="Page Count"
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col>
                                                        <b-form-group
                                                            label=""
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                </b-row>
                                                <b-row v-for="book in addAuthor.books" v-bind:key="book.key">
                                                    <b-col md="6">
                                                        <b-form-group>
                                                            <b-form-input
                                                                v-model="book.name"
                                                                placeholder="Book Name"
                                                                id="nested-bookname"
                                                            ></b-form-input>
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="4">
                                                        <b-form-group>
                                                            <b-form-input
                                                                v-model="book.pages_count"
                                                                placeholder="Page Count"
                                                                id="nested-pagecount"
                                                            ></b-form-input>
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="2">
                                                        <b-form-group>
                                                            <b-button
                                                                @click="handleBookDelete(book.id)"
                                                                variant="outline-danger"
                                                                >Del</b-button
                                                            >
                                                        </b-form-group>
                                                    </b-col>
                                                </b-row>
                                                <b-button @click="addNewBook()" variant="outline-secondary"
                                                    >Add new book</b-button
                                                >
                                            </b-form-group>
                                        </form>
                                    </b-modal>
                                </div>

                                <div>
                                    <b-modal
                                        id="modal-prevent-closing-edit"
                                        ref="modal"
                                        @show="resetModal"
                                        @hidden="resetModal"
                                        @ok="handleEdit"
                                        hide-backdrop
                                        content-class="shadow"
                                        title="Edit author"
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
                                                    v-model="editAuthor.name"
                                                    :state="nameState"
                                                    required
                                                ></b-form-input>
                                            </b-form-group>

                                            <b-form-group
                                                label-cols-lg="12"
                                                label="Books"
                                                label-size="md"
                                                label-class=" pt-0"
                                                class="mb-0"
                                            >
                                                <b-row v-if="editAuthor.books.length > 0">
                                                    <b-col md="6">
                                                        <b-form-group
                                                            label="Book Name"
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="6">
                                                        <b-form-group
                                                            label="Page Count"
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col>
                                                        <b-form-group
                                                            label=""
                                                            class="mb-0"
                                                            label-size="md"
                                                            label-class=" pt-0"
                                                        >
                                                        </b-form-group>
                                                    </b-col>
                                                </b-row>
                                                <b-row v-for="book in editAuthor.books" v-bind:key="book.key">
                                                    <b-col md="6">
                                                        <b-form-group>
                                                            <b-form-input
                                                                v-model="book.name"
                                                                placeholder="Book Name"
                                                                id="nested-bookname"
                                                            ></b-form-input>
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="4">
                                                        <b-form-group>
                                                            <b-form-input
                                                                v-model="book.pages_count"
                                                                placeholder="Page Count"
                                                                id="nested-pagecount"
                                                            ></b-form-input>
                                                        </b-form-group>
                                                    </b-col>
                                                    <b-col md="2">
                                                        <b-form-group>
                                                            <b-button
                                                                @click="handleEditBookDelete(book.id)"
                                                                variant="outline-danger"
                                                                >Del</b-button
                                                            >
                                                        </b-form-group>
                                                    </b-col>
                                                </b-row>
                                                <b-button @click="addNewBookOnEdit()" variant="outline-secondary"
                                                    >Add new book</b-button
                                                >
                                            </b-form-group>
                                        </form>
                                        <template #modal-footer="{ ok }" style="display: block">
                                            <b-button size="md" variant="outline-danger" @click="deleteAuthor()">
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
                            :items="authors"
                            :select-mode="single"
                            :fields="authorFields"
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
import PagesLayout from '../layouts/pages.vue';
export default {
    components: {
        PagesLayout,
    },
    data() {
        return {
            authorFields: ['name', 'count_of_books'],
            authors: [],
            bordered: true,
            query: '',
            addAuthor: {
                name: '',
                books: [],
            },
            nameState: null,
            books: [],
            editAuthor: {
                id: '',
                name: '',
                books: [],
            },
        };
    },

    methods: {
        getAuthors: async function () {
            const response = await this.$axios.get(`/authors?q=${this.query}`);
            this.authors = response.data;
        },
        deleteAuthor: async function () {
            const response = await this.$axios.delete(`/authors/${this.editAuthor.id}`);
            this.getAuthors();
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing-edit');
                this.clearSelected();
            });
        },
        saveAuthor: async function () {
            const response = await this.$axios.post('/authors', {
                name: this.addAuthor.name,
                books: this.addAuthor.books,
            });
            this.getAuthors();
        },
        saveChangesAuthor: async function () {
            const response = await this.$axios.put(`/authors/${this.editAuthor.id}`, {
                name: this.editAuthor.name,
                books: this.editAuthor.books,
            });
            this.getAuthors();
        },
        onSearch: function (event) {
            this.query = event.currentTarget.value;
            this.getAuthors();
        },
        checkFormValidity: function () {
            const valid = this.$refs.form.checkValidity();
            this.nameState = valid;
            return valid;
        },
        resetModal: function () {
            this.addAuthor.name = '';
            this.addAuthor.books = [];
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
            this.saveAuthor();
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
            this.saveChangesAuthor();
            // Hide the modal manually
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing-edit');
                this.clearSelected();
            });
        },
        onRowSelected: function (items) {
            if (items.length > 0) {
                this.editAuthor = items[0];
                this.$bvModal.show('modal-prevent-closing-edit');
            }
        },
        clearSelected: function () {
            this.$refs.selectableTable.clearSelected();
        },
        addNewBook: function () {
            const books = this.addAuthor.books.slice();
            const newBook = {
                name: '',
                id: books.length + 1,
                pages_count: 0,
            };
            books.push(newBook);
            this.addAuthor.books = books;
        },
        addNewBookOnEdit: function () {
            const books = this.editAuthor.books.slice();
            const newBook = {
                name: '',
                id: books.length + 1,
                pages_count: 0,
            };
            books.push(newBook);
            this.editAuthor.books = books;
        },
        handleBookDelete: function (rowId) {
            const books = this.addAuthor.books;
            const elementIndex = books.findIndex((element) => element.id === rowId);
            this.addAuthor.books.splice(elementIndex - 1, 1);
        },
        handleEditBookDelete: function (rowId) {
            const books = this.editAuthor.books;
            const elementIndex = books.findIndex((element) => element.id === rowId);
            this.editAuthor.books.splice(elementIndex - 1, 1);
        },
    },
    fetch() {
        this.getAuthors();
    },
};
</script>
