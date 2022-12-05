describe('Test login system', () => {
    it("test login study admin", () => {
        cy.visit("/");
        cy.url().should('include', '/login')

        cy.get("#username").type("sadmin");
        cy.get("#password").type("sadmin");
        cy.get("form").submit();
        cy.url().should('include', '/study-management/study-overview')

        cy.get("#logout").click()
        cy.url().should('include', '/login')
    }),
    it("test login study participant", () => {
        cy.visit("/");
      
        cy.get("#username").type("user");
        cy.get("#password").type("user");
        cy.get("form").submit();
        cy.url().should('include', '/study/login')

        cy.get("#logout").click()
        cy.url().should('include', '/login')
    }),
    it("test login user admin", () => {
        cy.visit("/");
      
        cy.get("#username").type("uadmin");
        cy.get("#password").type("uadmin");
        cy.get("form").submit();
        cy.url().should('include', '/user-management')

        cy.get("#logout").click()
        cy.url().should('include', '/login')
    })
})

  
