describe('Test study participation', () => {
    beforeEach(() => {
        cy.restoreLocalStorage();
    });
      
    afterEach(() => {
        cy.saveLocalStorage();
    });
    it("login study participant", () => {
        cy.visit("/");
        cy.url().should('include', '/login')

        cy.get("#username").type("user");
        cy.get("#password").type("user");
        cy.get("form").submit();
        cy.url().should('include', '/study/login')
    }),
    it("login into study", () => {
        cy.get("#studyId").type(1);
        cy.get("#password").type("test2");
        cy.get("form").submit();
        cy.url().should('include', '/study/1/participation')
    }),
    it("study particiaption", () => {
        // wait for modal to finish loading => otherwise cls btn not working
        cy.wait(1000)
        cy.get("#start-study").click()
        cy.wait(500)
        const scale_0_values = [3,6,1,1]
        const scale_1_values = [2,7,2,5]
        for (let i=0;i<4;i++) {
            cy.wait(200)
            cy.get("#scale-0").find('[type="radio"]').check(String(scale_0_values[i]))
            cy.get("#scale-1").find('[type="radio"]').check(String(scale_1_values[i]))
            cy.get("#votebtn-0").click()
        }
    }),
    it("close study and logout", () => {
        cy.get("#logout").click()
        cy.url().should('include', '/login')    
    }),
    it("login study participant", () => {
        cy.get("#username").type("test-user");
        cy.get("#password").type("test-user");
        cy.get("form").submit();
        cy.url().should('include', '/study/login')
    }),
    it("login into study with newl reg user", () => {
        cy.get("#studyId").type(1);
        cy.get("#password").type("test2");
        cy.get("form").submit();
        cy.url().should('include', '/study/1/participation')
    }),
    it("study particiaption user", () => {
        // wait for modal to finish loading => otherwise cls btn not working
        cy.wait(1000)
        cy.get("#start-study").click()
        cy.wait(500)
        const scale_0_values = [3,6,1,1]
        const scale_1_values = [2,7,2,5]
        for (let i=0;i<4;i++) {
            cy.wait(200)
            cy.get("#scale-0").find('[type="radio"]').check(String(scale_0_values[i]))
            cy.get("#scale-1").find('[type="radio"]').check(String(scale_1_values[i]))
            cy.get("#scale-0").find('[type="radio"]').check(String(scale_1_values[i]))
            cy.get("#scale-1").find('[type="radio"]').check(String(scale_0_values[i]))
            cy.get("#votebtn-0").click()
        }
    }),
    it("close study and logout", () => {
        cy.get("#logout").click()
        cy.url().should('include', '/login')    
    })
})