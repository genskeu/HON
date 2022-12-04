describe('Test create study', () => {
    beforeEach(() => {
        cy.restoreLocalStorage();
    });
      
    afterEach(() => {
        cy.saveLocalStorage();
    });
    it("login study admin", () => {
        cy.visit("/");
        cy.url().should('include', '/login')

        cy.get("#username").type("sadmin");
        cy.get("#password").type("sadmin");
        cy.get("form").submit();
    }),
    it("create study", () => {
        cy.get("#create-study").click();
        cy.url().should('include', '/metainfos')
        cy.get("#title").type("test raiting study 1")
        cy.get("#password").type("test1")
        cy.get("#description").type("this is a test study")
        cy.get("#save-meta").click()
    }),
    it("change study metainfos", () => {
        cy.get("#title").clear().type("test raiting study 1 mod")
        cy.get("#password").clear().type("test2")
        cy.get("#description").clear().type("this is still a test study")
        cy.get("#save-meta").click()
    }),
    it("upload files", () => {     
        cy.get("#fileupload").click()
        cy.get("#upload-modal").click()
        const files = ['cypress/files/0004_pre_group1/0004_pre_group1_0.dcm',
                       'cypress/files/0004_pre_group1/0004_pre_group1_1.dcm', 
                       'cypress/files/0004_pre_group1/0004_pre_group1_2.dcm',
                       'cypress/files/0004_pre_group1/0004_pre_group1_3.dcm']
        cy.get("#file-select").selectFile(files, { force: true })
        cy.get("#start-upload").click()
        // wait for upload to finish
        cy.wait(3000)
    }),
    it("create image-sets", () => {
        // wait for modal to finish loading => otherwise cls btn not working
        cy.wait(500)
        cy.get("#close-upload").click()
        cy.get("#design").click()
        cy.get("#acc-btn-man-imgsets").click()
        cy.get("#acc-btn-auto-imgsets").click()
        cy.get("#btn_auto_imgset").click()
        cy.get("#acc-btn-auto-imgsets").click()
    }),
    it("add scales", () => {     
        cy.get("#acc-scales-design").click()
        cy.get("#add_scale").click()
        cy.get("#add_scale").click()
        cy.get("#scaleText0").type("test scale 1")
        cy.get("#scaleText1").type("test scale 2")
        cy.get("#save-design").click()
    }),
    it("study preview", () => {     
        cy.get("#preview").click()
        // wait for modal to finish loading => otherwise cls btn not working
        cy.wait(500)
        cy.get("#start-study").click()
        cy.wait(500)
    })
})