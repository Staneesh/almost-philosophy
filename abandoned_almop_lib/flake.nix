{
  description = "Exploring Causal Relations in Data";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    overlay = (self: super: {
      python3 = super.python3.override {
        packageOverrides = pself: psuper: {
          slicer = psuper.slicer.overrideAttrs {
            # Skip test by overriding pytestCheckPhase
            pytestCheckPhase = "echo 'skipping tests'";
          };
          shap = psuper.shap.overrideAttrs {
            # Skip test by overriding pytestCheckPhase
            pytestCheckPhase = "echo 'skipping tests'";
          };
        };
      };
      python3Packages = self.python3.pkgs;
    });
    pkgs = (import nixpkgs) { inherit system; config.allowBroken = true; overlays = [ overlay ]; };

    econml = pkgs.python3Packages.buildPythonPackage rec {
        pname = "econml";
        version = "0.14.1";
        format = "pyproject";
        src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-yl6scJuBD3pCPyJRCoN3leKTc65tWajfx7anQ/zKR64=";
        };
        doCheck = false;
        nativeBuildInputs = [
            pkgs.python3Packages.poetry-core
            pkgs.python3Packages.setuptools-scm
        ];
        propagatedBuildInputs = [
          pkgs.python3Packages.joblib
          pkgs.python3Packages.graphviz
          pkgs.python3Packages.numpy
          pkgs.python3Packages.scipy
          pkgs.python3Packages.scikit-learn
          pkgs.python3Packages.sparse
          pkgs.python3Packages.statsmodels
          pkgs.python3Packages.pandas
          pkgs.python3Packages.shap
          pkgs.python3Packages.lightgbm
        ];
    };
    causal-learn = pkgs.python3Packages.buildPythonPackage rec{
        pname = "causal-learn";
        version = "0.1.3.6";
        src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-M2cp3nXv/ckLBBgO6chwPPrHm16AEvs9GT/sUealJIU=";
        };
        doCheck = false;
        # XD idk why, but unpacked source is not readable by default
        preBuild = ''
            ls -la
            chmod u+rw -R *
        '';
        propagatedBuildInputs = [
            pkgs.python3Packages.setuptools
            pkgs.python3Packages.pandas
            pkgs.python3Packages.tqdm
            pkgs.python3Packages.scipy
            pkgs.python3Packages.networkx
            pkgs.python3Packages.scikit-learn
            pkgs.python3Packages.statsmodels
            pkgs.python3Packages.pydot
            pkgs.python3Packages.graphviz
        ];
    };
    dowhy = pkgs.python3Packages.buildPythonPackage rec{
        pname = "dowhy";
        version = "0.10.1";
        src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-4tz36VqYxEWxQqnYMklqeM3HWtTNPz45N6mHRjrW594=";
        };
        format = "pyproject";
        nativeBuildInputs = [
            pkgs.python3Packages.poetry-core
            pkgs.python3Packages.setuptools-scm
        ];
        propagatedBuildInputs = [
            causal-learn
            econml

            pkgs.python3Packages.joblib
            pkgs.python3Packages.cvxpy
            pkgs.python3Packages.cython
            pkgs.python3Packages.scipy
            pkgs.python3Packages.statsmodels
            pkgs.python3Packages.numpy
            pkgs.python3Packages.pandas
            pkgs.python3Packages.networkx
            pkgs.python3Packages.sympy
            pkgs.python3Packages.scikit-learn
            pkgs.python3Packages.pydot
            pkgs.python3Packages.pygraphviz
            pkgs.python3Packages.tqdm
            pkgs.python3Packages.matplotlib
            pkgs.python3Packages.cvxpy
        ];
    };
    python-packages = ps: with ps; [
        numpy
        matplotlib
        pandas
        dowhy
      ];
    my-python-env = pkgs.python3.withPackages python-packages;
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        my-python-env
      ];
    };
  };
}
