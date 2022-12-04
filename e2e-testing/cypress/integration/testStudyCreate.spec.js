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
    }),
    it("create image-sets", () => {     
    }),
    it("add scales", () => {     
    })
})