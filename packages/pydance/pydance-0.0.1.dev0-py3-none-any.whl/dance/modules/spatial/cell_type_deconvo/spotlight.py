import numpy as np
from sklearn.decomposition import NMF
from sklearn.linear_model import LinearRegression

def cell_topic_profile(X, groups, axis=1, method='median'):
    """cell_topic_profile.

    Parameters
    ----------
    X : numpy 2-d array
        gene expression matrix, genes (rows) by sample cells (cols).
    groups : int
        cell-type labels of each sample cell in X.
    method : string optional
         method for reduction of cell-types for cell profile, default median.
           
    Returns
        -------
    X_profile : numpy 2-d array
         cell profile matrix from scRNA-seq reference.

    """
    groups = np.array(groups)
    ids=np.unique(groups)
    if method == "median":
        X_profile = np.array([np.median(X[:, groups==ids[i]], axis=1) for i in range(len(ids))]).T
    else:
        X_profile = np.array([np.mean(X[:, groups==ids[i]], axis=1) for i in range(len(ids))]).T
    return X_profile
    
    
class SPOTlight(object):    
    """SPOTlight class.

    Parameters
    ----------
    rank : int
           rank of the matrix factorization.
    bias : boolean optional
           set true to include bias term in the regression modules, default False.
    profile_mtd : string optional
           method for reduction of cell-types for cell profile, default median.
    init : string optional
           initialization method for matrix factorization solver (see NMF from sklearn).
    max_iter : int optional
           maximum iterations allowed for matrix factorization solver.
    
    Returns
        -------
    None.

    """
    def __init__(self, rank, bias=False, profile_mtd='median', init='random', random_state=0, max_iter=1000):
        super(SPOTlight, self).__init__()
        self.bias = bias
        self.profile_mtd = 'median'
        
        self.nmf_model = NMF(n_components=rank, init=init,  random_state=random_state, max_iter=max_iter)

        self.nnls_reg1=LinearRegression(fit_intercept=bias,positive=True)

        self.nnls_reg2=LinearRegression(fit_intercept=bias,positive=True)
    
    def fit(self,x,y, cell_types):
        """fit function for model training.

        Parameters
        ----------
        x : 
            scRNA-seq reference expression.
        y : 
            mixed cell expression to be deconvoluted.
        cell_types : 
            cell type annotations for scRNA-seq reference.
            
        Returns
        -------
        None.

        """
        #1. run NMF on scRNA X
        self.W = self.nmf_model.fit_transform(x)
        self.H = self.nmf_model.components_
        
        #2. get cell-topic and mix-topic profiles
        #a. get cell-topic profiles H_profile: cell-type group medians of coef H (topic x cells)
        self.H_profile = cell_topic_profile(self.H, groups=cell_types,axis=1, method=self.profile_mtd)
        
        #b. get mix-topic profiles B: NNLS of basis W onto mix expression Y -- y ~ W*b
        #nnls ran for each spot
        self.nnls_reg1.fit(self.W, y)
        self.B=self.nnls_reg1.coef_.T
        
        #3.  get cell-type proportions P: NNLS of cell-topic profile H_profile onoto mix-topic profile B -- b ~ h_profile*p 
        self.nnls_reg2.fit(self.H_profile, self.B)
        self.P=self.nnls_reg2.coef_.T
        
    def predict(self, y):
        """prediction function.
        Parameters
        ----------
        y : numpy 2-d array
            mixed cell expression.
        
        Returns
        -------
        P : numpy 2-d array
            predictions of cell-type proportions.
        
        """
        nnls = LinearRegression(fit_intercept=self.bias,positive=True)
        nnls.fit(self.W, y)
        B=nnls.coef_.T
        
        nnls = LinearRegression(fit_intercept=self.bias,positive=True)
        nnls.fit(self.H_profile, B)
        P=nnls.coef_.T
        return(P)
    
    def score(self, x, y, cell_types):
        """score.

        Parameters
        ----------
        x : 
            scRNA-seq reference expression.
        y : 
            mixed cell expression to be deconvoluted.
        cell_types : 
            cell type annotations for scRNA-seq reference.

        Returns
        -------
        model_score : float
            coefficient of determination of the prediction (final non-negative linear module).

        """
        self.fit(x,y,cell_types)
        model_score = self.nnls_reg2.score(self.H_profile, self.B)
        return model_score
        
        